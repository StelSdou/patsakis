import shutil
import tempfile

import httpx
from fastapi import FastAPI, File, UploadFile, Request, Form
import uvicorn
from starlette.middleware.cors import CORSMiddleware
import algorithm

app_fastapi = FastAPI()

app_fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

async def algor(path: str):
    url = "http://127.0.0.1:5000/"
    data = algorithm.Algorithm(path)
    async with httpx.AsyncClient() as client:
        response = await client.post(url + "getImgJson", json=data["metadata"])
        response.raise_for_status()
    # return {"status": "data sent", "response": response.json()}

    encoded = data["image"]
    image = [encoded[i:i + 12] for i in range(0, len(encoded), 12)]
    async with httpx.AsyncClient() as client:
        for i, img in enumerate(image):
            payload = {
                "chunk": img,
                "index": i,
                "total": len(image)
            }
            response = await client.post(url + "getImg", json=payload)
            print(f"Sent chunk {i + 1}/{len(image)}: {img} —> {((i + 1) / len(image)) * 100:.2f}% complete")
@app_fastapi.post("/")
def handle_root_post():
    return {"status": "ok"}

@app_fastapi.post("/send")
async def send(path: str = Form(...)):
    await algor(path)

    return {"status": "ok"}

@app_fastapi.post("/sendWithUi")
async def send(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        path = tmp.name

    await algor(path)

    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app_fastapi, port=8000)