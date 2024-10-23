from flask import Flask, render_template, request
from PIL import Image
from compress_image import compress_image

app: Flask = Flask(__name__)

@app.route("/", methods=["GET"])
def index() -> str:
    print(request)
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_image() -> str:
    PATH: str = "static/uploaded_image.jpg"
    print(request)
    file = request.files["image"]
    file.save(PATH)
    return PATH

if __name__ == "__main__":
    app.run()
