import numpy as np
import onnxruntime
from PIL import Image
from typing import Optional, Union, Tuple


class InferWorker(object):
    def __init__(self, 
                 onnx_file: Optional[str] = "weight/bisenet_v2_512x512_rs_building.onnx", 
                 size: Union[Tuple, int] = 512) -> None:
        super(InferWorker, self).__init__()
        if onnx_file is not None:
            self.ort_sess = onnxruntime.InferenceSession(onnx_file)
        self.size = (size, size) if isinstance(size, int) else size
        _mean=[0.5] * 3
        _std=[0.5] * 3
        self._mean = np.float32(np.array(_mean).reshape(-1, 1, 1))
        self._std = np.float32(np.array(_std).reshape(-1, 1, 1))

    def load_model(self, onnx_file: str) -> None:
        self.ort_sess = onnxruntime.InferenceSession(onnx_file)

    def __preprocess(self, img: Union[np.ndarray, Image.Image, str]) -> np.ndarray:
        if isinstance(img, str):
            img = np.asarray(Image.open(img))
        elif isinstance(img, Image.Image):
            img = np.asarray(img)
        h, w = img.shape[:2]
        tmp = np.zeros((self.size[0], self.size[1], 3), dtype="uint8")
        tmp[:h, :w, :] = img
        img = np.asarray(Image.fromarray(tmp).resize(self.size, resample=Image.CUBIC))
        img = (img.astype("float32") / 255.).transpose((2, 0, 1))
        img = (img - self._mean) / self._std
        C, H, W = img.shape
        img = img.reshape([1, C, H, W])
        return img

    def infer(self, 
              img: Union[np.ndarray, str], 
              mul_255: bool = True) -> Image.Image:
        x = self.__preprocess(img)
        ort_inputs = {self.ort_sess.get_inputs()[0].name: x}
        ort_outs = self.ort_sess.run(None, ort_inputs)
        result = np.squeeze(np.argmax(ort_outs[0], axis=1).astype("uint8"))
        if mul_255 is True:
           result *= 255
        return Image.fromarray(result)
