from fastapi import FastAPI, Form
from fastapi import Request

from range_response import range_requests_response

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}

@app.get("/video")
def get_video(request: Request):
    return range_requests_response(
        request, file_path="/home/ev/Downloads/[Udemy] Python 3 Deep Dive (Part 1 – Functional) (08.2020)/07 Scopes, Closures and Decorators/001 Introduction.mp4", content_type="video/mp4"
    )
