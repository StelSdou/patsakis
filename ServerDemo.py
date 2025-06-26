from flask import Flask, jsonify, request, render_template
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)















# @app.route("/api", methods=['POST'])
# def api():
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "No data provided"}), 400
#     encoded_message = data.get("encoded_message", "0123456789abcdef")
#     compression_algorithm = data.get("compression_algorithm", "lz77/lz78/fano-shannon/huffman")
#     encoding = data.get("encoding", "linear/cyclic/orthogonal")
#     parameters = data.get("parameters", "[param_list]")
#     errors = data.get("errors", "n")
#     SHA256 = data.get("SHA256", "h")
#     entropy = data.get("entropy", "e")
#
#     return jsonify({"message": f"{encoded_message} \n {compression_algorithm} \n {encoding} \n {parameters} \n {errors} \n {SHA256} \n {entropy}"})

# {
#   “encoded_message”: “0123456789abcdef”,
#   “compression_algorithm”: “lz77/lz78/fano-shannon/huffman”,
#   “encoding”: “linear/cyclic/orthogonal”,
#   “parameters”:[param_list],
#   “errors”: n,
#   “SHA256”: h,
#   "entropy":e
# }