from flask import Flask, render_template, request, jsonify
from PIL import Image
from compress_image import compress_image
import os

app: Flask = Flask(__name__)

@app.route("/", methods=["GET"])
def index() -> str:
    print(request)
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_image() -> dict:
    PATH: str = "static/compressed_image.jpg"

    print(request)

    # Get data from the form
    file = request.files["image"]
    image: Image = Image.open(file)
    quality: float = float(request.form["quality"]) / 100
    
    compressed_image: Image = compress_image(image, quality)
    compressed_image.save(PATH)

    compressed_size: int = os.path.getsize(PATH)

    return jsonify({
        "compressed_path": PATH,
        "compressed_size": format_size(compressed_size)
    })

def format_size(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} GB"

if __name__ == "__main__":
    app.run()