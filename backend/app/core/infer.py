import paddle
from paddle.io import DistributedBatchSampler, DataLoader
from paddlenlp.data import Tuple, Pad
from paddlenlp.datasets import load_dataset
from paddlenlp.transformers import ErnieTokenizer
from paddlenlp.transformers import ErnieForGeneration
import jieba
import numpy as np
from functools import partial
from .utils import convert_example, after_padding
from typing import Dict


def gen_bias(encoder_inputs, decoder_inputs, step):
    decoder_bsz, decoder_seqlen = decoder_inputs.shape[:2]
    encoder_bsz, encoder_seqlen = encoder_inputs.shape[:2]
    attn_bias = paddle.reshape(
        paddle.arange(
            0, decoder_seqlen, 1, dtype="float32") + 1, [1, -1, 1])
    decoder_bias = paddle.cast(
        (paddle.matmul(
            attn_bias, 1. / attn_bias, transpose_y=True) >= 1.),
        "float32")  # [1, decoderlen, decoderlen]
    encoder_bias = paddle.unsqueeze(
        paddle.cast(paddle.ones_like(encoder_inputs), "float32"),
        [1])  # [bsz, 1, encoderlen]
    encoder_bias = paddle.expand(
        encoder_bias, [encoder_bsz, decoder_seqlen,
                       encoder_seqlen])  # [bsz,decoderlen, encoderlen]
    decoder_bias = paddle.expand(
        decoder_bias, [decoder_bsz, decoder_seqlen,
                       decoder_seqlen])  # [bsz, decoderlen, decoderlen]
    if step > 0:
        bias = paddle.concat([
            encoder_bias, paddle.ones([decoder_bsz, decoder_seqlen, step],
                                      "float32"), decoder_bias
        ], -1)
    else:
        bias = paddle.concat([encoder_bias, decoder_bias], -1)
    return bias


@paddle.no_grad()
def greedy_search_infilling(model,
                            q_ids,
                            q_sids,
                            sos_id,
                            eos_id,
                            attn_id,
                            pad_id,
                            unk_id,
                            vocab_size,
                            max_encode_len=300,
                            max_decode_len=120,
                            tgt_type_id=3):
    _, logits, info = model(q_ids, q_sids)
    d_batch, d_seqlen = q_ids.shape
    seqlen = paddle.sum(paddle.cast(q_ids != 0, "int64"), 1, keepdim=True)
    has_stopped = np.zeros([d_batch], dtype=np.bool)
    gen_seq_len = np.zeros([d_batch], dtype=np.int64)
    output_ids = []
    past_cache = info["caches"]
    cls_ids = paddle.ones([d_batch], dtype="int64") * sos_id
    attn_ids = paddle.ones([d_batch], dtype="int64") * attn_id
    ids = paddle.stack([cls_ids, attn_ids], -1)
    for step in range(max_decode_len):
        bias = gen_bias(q_ids, ids, step)
        pos_ids = paddle.to_tensor(
            np.tile(
                np.array(
                    [[step, step + 1]], dtype=np.int64), [d_batch, 1]))
        pos_ids += seqlen
        _, logits, info = model(
            ids,
            paddle.ones_like(ids) * tgt_type_id,
            pos_ids=pos_ids,
            attn_bias=bias,
            past_cache=past_cache)
        if logits.shape[-1] > vocab_size:
            logits[:, :, vocab_size:] = 0
        logits[:, :, pad_id] = 0
        logits[:, :, unk_id] = 0
        logits[:, :, attn_id] = 0
        gen_ids = paddle.argmax(logits, -1)
        past_cached_k, past_cached_v = past_cache
        cached_k, cached_v = info["caches"]
        cached_k = [
            paddle.concat([pk, k[:, :1, :]], 1)
            for pk, k in zip(past_cached_k, cached_k)
        ]  # concat cached 
        cached_v = [
            paddle.concat([pv, v[:, :1, :]], 1)
            for pv, v in zip(past_cached_v, cached_v)
        ]
        past_cache = (cached_k, cached_v)

        gen_ids = gen_ids[:, 1]
        ids = paddle.stack([gen_ids, attn_ids], 1)
        gen_ids = gen_ids.numpy()
        has_stopped |= (gen_ids == eos_id).astype(np.bool)
        gen_seq_len += (1 - has_stopped.astype(np.int64))
        output_ids.append(gen_ids.tolist())
        if has_stopped.all():
            break
    output_ids = np.array(output_ids).transpose([1, 0])
    return output_ids


class InferWorker:
    def __init__(self, model_and_tokenizer_dir: str) -> None:
        paddle.set_device("gpu")
        # load
        self.tokenizer = ErnieTokenizer.from_pretrained(model_and_tokenizer_dir)
        self.model = ErnieForGeneration.from_pretrained(model_and_tokenizer_dir)
        self.vocab = self.tokenizer.vocab
        self.eos_id = self.vocab[self.tokenizer.sep_token]
        self.sos_id = self.vocab[self.tokenizer.cls_token]
        self.pad_id = self.vocab[self.tokenizer.pad_token]
        self.unk_id = self.vocab[self.tokenizer.unk_token]
        self.vocab_size = len(self.vocab)
        self.model.eval()
        
    def create_title(self, abstract: str) -> Dict:
        evaluated_sentences_ids = []
        evaluated_sentences = []
        # data processing
        temp_abstract = jieba.lcut(abstract)
        def read():
            yield {"abstract": "\x02".join(temp_abstract), "title": ""}
        infer_ds = load_dataset(read, lazy=False)
        attn_id = self.vocab["[MASK]"]
        tgt_type_id = 1
        max_encode_len = 300
        max_decode_len = 120
        infer_trans_func = partial(
            convert_example,
            tokenizer=self.tokenizer,
            attn_id=attn_id,
            tgt_type_id=tgt_type_id,
            max_encode_len=max_encode_len,
            max_decode_len=max_decode_len
        )
        infer_ds = infer_ds.map(infer_trans_func, lazy=False, num_workers=0)
        infer_batch_sampler = DistributedBatchSampler(infer_ds, batch_size=1)
        infer_collate_fn = lambda samples, fn=Tuple(
            Pad(axis=0, pad_val=self.tokenizer.pad_token_id),  # src_ids
            Pad(axis=0, pad_val=self.tokenizer.pad_token_id),  # src_pids
            Pad(axis=0, pad_val=self.tokenizer.pad_token_type_id),  # src_sids
            Pad(axis=0, pad_val=self.tokenizer.pad_token_id),  # tgt_ids
            Pad(axis=0, pad_val=self.tokenizer.pad_token_id),  # tgt_pids
            Pad(axis=0, pad_val=self.tokenizer.pad_token_type_id),  # tgt_sids
            Pad(axis=0, pad_val=self.tokenizer.pad_token_id),  # attn_ids
            Pad(axis=0, pad_val=self.tokenizer.pad_token_id),  # tgt_labels
        ): after_padding(fn(samples))
        # 构造DataLoader
        infer_data_loader = DataLoader(
            dataset=infer_ds,
            batch_sampler=infer_batch_sampler,
            collate_fn=infer_collate_fn,
            return_list=True
        )
        for data in infer_data_loader:
            src_ids, src_sids, src_pids = data[:3]  # never use target when infer
            output_ids = greedy_search_infilling(
                self.model,
                src_ids,
                src_sids,
                eos_id=self.eos_id,
                sos_id=self.sos_id,
                attn_id=attn_id,
                pad_id=self.pad_id,
                unk_id=self.unk_id,
                vocab_size=self.vocab_size,
                max_decode_len=max_decode_len,
                max_encode_len=max_encode_len,
                tgt_type_id=tgt_type_id)
            for ids in output_ids.tolist():
                if self.eos_id in ids:
                    ids = ids[:ids.index(self.eos_id)]
                evaluated_sentences_ids.append(ids)
        for ids in evaluated_sentences_ids[:5]:
            evaluated_sentences.append("".join(self.vocab.to_tokens(ids)))
        return {"abstract": abstract, "title": evaluated_sentences}
