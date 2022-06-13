import os.path as osp
import uvicorn
from fastapi import FastAPI
from typing import Dict
from core import InferWorker


PATH = osp.abspath(osp.dirname(osp.dirname(__file__)))


app = FastAPI()
infer_worker = InferWorker(osp.join(PATH, "weight"))
title = ""


@app.get("/")
async def ping() -> Dict:
    return {"ping": "pong!"}


@app.post("/predict")
async def predict(data: Dict) -> None:
    abstract = data["abstract"]
    pred = infer_worker.create_title(abstract)
    global title
    title = pred["title"]


@app.get("/result")
async def output() -> Dict:
    return {"title": title}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
