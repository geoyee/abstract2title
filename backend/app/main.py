import os.path as osp
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from core import InferWorker
from typing import Dict


PATH = osp.abspath(osp.dirname(osp.dirname(__file__)))


app = FastAPI()
infer_worker = InferWorker(osp.join(PATH, "weight"))


origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def ping() -> Dict:
    return {"ping": "pong!"}


@app.post("/predict")
async def predict(data: Request) -> Dict:
    data = await data.json()
    abstract = data["abstract"]
    pred = infer_worker.create_title(abstract)
    title = pred["title"]
    return {"title": title}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
