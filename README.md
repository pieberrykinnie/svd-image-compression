# Image Compressor

An image compressor using singular value decomposition (SVD) to reduce image file sizes. Built with NumPy and Flask.

Currently, the output image is grayscale. More options will be added in the future.

## Live Demo

Try it out at: https://svd-image-compression.fly.dev

## Features

- Upload any JPG/PNG image
- Adjust compression quality with a slider
- Compare original vs compressed images side-by-side
- Download compressed result

## Run Locally

1. Clone this repository:

```bash
git clone https://github.com/pieberrykinnie/svd-image-compression.git
```

2. Run a Python virtual environment:

Create a virtual environment:

```bash
python3 -m venv .venv
```

OR

```bash
python -m venv .venv
``` 

Activate the virtual environment:

```bash
.venv/bin/activate # On Mac/Linux
```

OR

```bash
.venv\Scripts\activate # On Windows 
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Flask app:

```bash
python3 app.py
```

OR

```bash
python app.py
```

5. Open your browser and navigate to:

```bash
http://localhost:8080
```