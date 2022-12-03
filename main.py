from flask import Flask, request, jsonify
from easyocr import Reader
from PIL import Image
from flask_cors import CORS

def image_2_text(image_path, langs=["en"]):
  image = Image.open(image_path)
  reader = Reader(langs)
  resp = []
  results = reader.readtext(image)
  for (bbox, text, prob) in results:
    resp = resp.append(text)
    print("[INFO] {:.4f}: {}".format(prob, text)) 
    print("resp", resp)
    # unpack the bounding box


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/", methods=["GET"])
def hello():
    return 'hello'

@app.route("/post-image", methods=["POST"])
def receive_image():
    file = request.files['image']
    # Read the image via file.stream
    img = Image.open(file.stream)
    file.save("image.jpg")
    image_2_text("./image.jpg", ["en"])

    return jsonify({'msg': 'success', 'size': [img.width, img.height]})
