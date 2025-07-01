from typing import Dict, Any

from annotated_types.test_cases import cases
from flask import Flask, jsonify, request, render_template
from pydantic import BaseModel
import base64
import os

class DataModel(BaseModel):
    encoded_message: str
    compression_algorithm: str
    encoding: str
    parameters: Dict[str, Any]
    errors: int
    SHA256: str
    entropy: str


app_flask = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = None
received_chunks = {}
image = ""

def check(final):
    p = 0
    while (2 ** p) < (p + 8 + 1):
        p += 1

    d = list(final.decode())
    error = 0
    for i in range(p):
        parity_pos = 2 ** i
        parity = 0
        for j in range(1, len(d) + 1):
            if j & parity_pos:
                parity ^= int(d[j - 1])
        if parity != 0:
            error += parity_pos

    if error > 0:
        print("Error Position:", error)
        d[error - 1] = '1' if d[error - 1] == '0' else '0'

    decoded = []
    for i in range(1, len(d) + 1):
        if not (i & (i - 1)) == 0:
            decoded.append(d[i - 1])

    # print (''.join(decoded))
    return ''.join(decoded)

@app_flask.route("/", methods=["GET", "POST"])
def home():
    return render_template('index.html')

@app_flask.route("/test", methods=["GET", "POST"])
def test():
    return {"message": "test ok"}

@app_flask.route("/getImgJson", methods=["POST"])
def getImgJson():
    data = request.get_json()
    global model
    if not data:
        return jsonify({"error": "No JSON received"}), 400
    try:
        model = DataModel(**data)
    except Exception as e:
        return jsonify({"error": e.errors()}), 422

    return jsonify({"message": "data received", "received": "ok"})


@app_flask.route("/getImg", methods=["POST"])
def getImg():
    global model, image
    data = request.get_json()
    index = data.get("index")
    total = data.get("total")
    chunk = data.get("chunk")

    if index is None or chunk is None:
        return jsonify({"error": "Missing data"}), 400

    image += check(chunk.encode())
    received_chunks[index] = chunk
    if len(received_chunks) == total:
        message = ''.join(received_chunks[i] for i in range(total))
        print("Full message received")
        received_chunks.clear()
        if base64.b64encode(message.encode()).decode() == model.SHA256:
            reverse_map = {v: k for k, v in model.parameters.items()}
            decoded_bytes = bytearray()
            current_code = ""
            for bit in image:
                current_code += bit
                if current_code in reverse_map:
                    # print(type(reverse_map[current_code]), reverse_map[current_code])

                    decoded_bytes.append(int(reverse_map[current_code]))
                    current_code = ""

            print (bytes(decoded_bytes))
            with open("uploads/out.png", "wb") as f:
                f.write(decoded_bytes)


    name = "stelios"
    return render_template('verify.html', name=name)
    # return jsonify({"status": "chunk received", "index": index})


if __name__ == "__main__":
    app_flask.run(debug=True)