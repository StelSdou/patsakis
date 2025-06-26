from fastapi import FastAPI, File, UploadFile, Request
import uvicorn
from starlette.middleware.cors import CORSMiddleware
import requests
from PIL import Image
import io
import magic
import base64


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# FLASK_SERVER_URL = "http://127.0.0.1:5000/upload"
@app.post("/")
def handle_root_post():
    return {"status": "ok"}

@app.post("/process")
async def process(fileElem: UploadFile = File(...)):
    contents = await fileElem.read()

    size = len(contents)
    print(size)
    return {
        "filename": fileElem.filename,
        "content_type": fileElem.content_type,
        "size": size
    }


if __name__ == "__main__":
    uvicorn.run(app, port=8000)




# # 1. MIME type έλεγχος
    # mime = magic.from_buffer(content, mime=True)
    # if not mime.startswith("image/"):
    #     return "Το αρχείο δεν είναι εικόνα."
    #
    # # 2. Άνοιγμα εικόνας (π.χ. για χειρισμό)
    # image = Image.open(io.BytesIO(content))
    # image = image.convert("RGB")  # π.χ. μετατροπή
    #
    # # 3. Συμπίεση – π.χ. αποθήκευση σε JPEG buffer
    # output_buffer = io.BytesIO()
    # image.save(output_buffer, format="JPEG", quality=50)
    # compressed_data = output_buffer.getvalue()
    #
    # # 4. Αποστολή στον Flask server
    # files = {'fileElem': ('compressed.jpg', compressed_data, 'image/jpeg')}
    # response = requests.post(FLASK_SERVER_URL, files=files)
    #
    # return f"Απεστάλη στο Flask server με status {response.status_code}"