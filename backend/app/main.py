import uvicorn
from fastapi import FastAPI, UploadFile, File
from typing import Dict
from core import InferWorker, read_imagefile, image_to_base64


app = FastAPI()
infer_worker = InferWorker()
segmentation = ""


@app.get("/")
async def ping() -> Dict[str, str]:
    return {"ping": "pong!"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> None:
    ext = file.filename.split(".")[-1]
    if ext not in ["jpg", "jpeg"]:
        raise ValueError("Image must be jpg/jpeg format!")
    img = read_imagefile(await file.read())
    pred = infer_worker.infer(img)
    global segmentation 
    segmentation = image_to_base64(pred)


@app.get("/result")
async def output() -> Dict[str, str]:
    return {"segmentation": segmentation}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
