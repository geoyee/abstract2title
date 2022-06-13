import numpy as np
from copy import deepcopy
from typing import Dict, Tuple, Optional


def convert_example(
    example: Dict,
    tokenizer,
    attn_id,
    tgt_type_id,
    max_encode_len: int,
    max_decode_len: int,
) -> Tuple:
    """convert an example into necessary features"""
    encoded_src = tokenizer.encode(
        example["abstract"], max_seq_len=max_encode_len, pad_to_max_seq_len=False
    )
    src_ids, src_sids = encoded_src["input_ids"], encoded_src["token_type_ids"]
    src_pids = np.arange(len(src_ids))
    encoded_tgt = tokenizer.encode(
        example["title"], max_seq_len=max_decode_len, pad_to_max_seq_len=False
    )
    tgt_ids, tgt_sids = encoded_tgt["input_ids"], encoded_tgt["token_type_ids"]
    tgt_ids = np.array(tgt_ids)
    tgt_sids = np.array(tgt_sids) + tgt_type_id
    tgt_pids = np.arange(len(tgt_ids)) + len(src_ids)
    attn_ids = np.ones_like(tgt_ids) * attn_id
    tgt_labels = tgt_ids
    return (
        src_ids,
        src_pids,
        src_sids,
        tgt_ids,
        tgt_pids,
        tgt_sids,
        attn_ids,
        tgt_labels,
    )


def gen_mask(
    batch_ids: np.ndarray,
    mask_type: str = "bidi",
    query_len: Optional[int] = None,
    pad_value: int = 0,
) -> np.ndarray:
    if query_len is None:
        query_len = batch_ids.shape[1]
    if mask_type != "empty":
        mask = (batch_ids != pad_value).astype(np.float32)
        mask = np.tile(np.expand_dims(mask, 1), [1, query_len, 1])
        if mask_type == "causal":
            assert query_len == batch_ids.shape[1]
            mask = np.tril(mask)
        elif mask_type == "causal_without_diag":
            assert query_len == batch_ids.shape[1]
            mask = np.tril(mask, -1)
        elif mask_type == "diag":
            assert query_len == batch_ids.shape[1]
            mask = np.stack([np.diag(np.diag(m)) for m in mask], 0)
    else:
        mask_type == "empty"
        mask = np.zeros_like(batch_ids).astype(np.float32)
        mask = np.tile(np.expand_dims(mask, 1), [1, query_len, 1])
    return mask


def after_padding(args: Tuple) -> Tuple:
    (
        src_ids,
        src_pids,
        src_sids,
        tgt_ids,
        tgt_pids,
        tgt_sids,
        attn_ids,
        tgt_labels,
    ) = args
    src_len = src_ids.shape[1]
    tgt_len = tgt_ids.shape[1]
    mask_00 = gen_mask(src_ids, "bidi", query_len=src_len)
    mask_01 = gen_mask(tgt_ids, "empty", query_len=src_len)
    mask_02 = gen_mask(attn_ids, "empty", query_len=src_len)
    mask_10 = gen_mask(src_ids, "bidi", query_len=tgt_len)
    mask_11 = gen_mask(tgt_ids, "causal", query_len=tgt_len)
    mask_12 = gen_mask(attn_ids, "empty", query_len=tgt_len)
    mask_20 = gen_mask(src_ids, "bidi", query_len=tgt_len)
    mask_21 = gen_mask(tgt_ids, "causal_without_diag", query_len=tgt_len)
    mask_22 = gen_mask(attn_ids, "diag", query_len=tgt_len)
    mask_src_2_src = mask_00
    mask_tgt_2_srctgt = np.concatenate([mask_10, mask_11], 2)
    mask_attn_2_srctgtattn = np.concatenate([mask_20, mask_21, mask_22], 2)
    raw_tgt_labels = deepcopy(tgt_labels)
    tgt_labels = tgt_labels[np.where(tgt_labels != 0)]
    return (
        src_ids,
        src_sids,
        src_pids,
        tgt_ids,
        tgt_sids,
        tgt_pids,
        attn_ids,
        mask_src_2_src,
        mask_tgt_2_srctgt,
        mask_attn_2_srctgtattn,
        tgt_labels,
        raw_tgt_labels,
    )
