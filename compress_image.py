import numpy as np
from typing import List
from PIL import Image

def svd(m: np.ndarray) -> dict:
    """Given a matrix, return the singular value decomposition of the matrix."""
    
    # Compute eigenvalues and eigenvectors of M^T * M
    mtm: np.ndarray = np.matmul(m.T, m)
    ev: np.ndarray = np.linalg.eig(mtm)

    # Reorder the eigenvalues and corresponding eigenvectors in decreasing order
    indices: List[int] = np.argsort(ev[0])[::-1]
    ev_values: np.ndarray = ev[0][indices]
    ev_vectors: np.ndarray = ev[1][:, indices]

    # Find the index of the first close-to-zero eigenvalue (if any)
    for i in range(len(ev_values)):
        if ev_values[i] < 1e-10:
            break

    # Compute the singular values of non-zero eigenvalues
    sv: np.ndarray = np.sqrt(ev_values[:i])

    # Construct the scaling matrix
    s: np.ndarray = np.zeros(m.shape)
    for j in range(min(i, m.shape[0], m.shape[1])):
        s[j, j] = sv[j]
    
    # Construct the singular vectors
    v: np.ndarray = ev_vectors

    u: np.ndarray = np.zeros((m.shape[0], m.shape[0]))
    for j in range(i):
        u[:, j] = np.matmul(m, v[:, j]) / sv[j]

    # Ensure U has no missing columns
    if i < m.shape[0]:
        mmt: np.ndarray = np.matmul(m, m.T)
        ev2: np.ndarray = np.linalg.eig(mmt)
        indices2: List[int] = np.argsort(ev2[0])[::-1]
        ev2_vectors: np.ndarray = ev2[1][:, indices2]

        for j in range(i, m.shape[0]):
            u[:, j] = ev2_vectors[:, j]

    return {"S": s, "U": u, "V": v, "D": sv}

def compress_image(image: Image, quality: float) -> Image:
    """Given an image, convert it to grayscale and compress it to a certain quality level given between 0 and 1."""
    assert(0 <= quality and quality <= 1)

    # Convert the image to grayscale, then to a numpy matrix
    grayscale_image: Image = image.convert("L")
    image_matrix: np.ndarray = np.array(grayscale_image)

    # Call the singular value decomposition function on the matrix
    svd_result: dict = svd(image_matrix)

    # Use quality to determine how many singular values to keep
    n: int = round(quality * len(svd_result["D"]))
    
    # Construct the compressed matrix
    u_new: np.ndarray = svd_result["U"][:, :n]
    v_new: np.ndarray = svd_result["V"][:, :n]

    s_new: np.ndarray = np.zeros((u_new.shape[0], v_new.shape[0]))

    for i in range(n):
        s_new += svd_result["D"][i] * np.outer(u_new[:, i], v_new[:, i])
        # s_new += svd_result["D"][i] * np.matmul(u_new[:, :i], v_new[:, :i].T)

    # Rescale the values of the matrix to be between 0 and 1
    if (np.min(s_new) < 0):
        s_new -= np.min(s_new)
    s_new /= np.max(s_new)

    # Convert the numpy matrix back to a grayscale image
    s_new = (s_new * 255).astype(np.uint8)  # Scale to 0-255 and convert to uint8
    compressed_image: Image = Image.fromarray(s_new, mode="L")

    return compressed_image

# Example usage
image: Image = Image.open("IMG_9714.jpg")
image.convert("L").save("grayscale_image.jpg", "JPEG")
compressed_image: Image = compress_image(image, 0.5)
compressed_image.save("compressed_image.jpg", "JPEG")