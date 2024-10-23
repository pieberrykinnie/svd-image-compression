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
    PATH: str = "static/compressed_image.jpg"

    print(request)

    # Get data from the form
    file = request.files["image"]
    image: Image = Image.open(file)
    quality: float = float(request.form["quality"]) / 100
    
    compressed_image: Image = compress_image(image, quality)
    compressed_image.save(PATH)
    return PATH

if __name__ == "__main__":
    app.run()
