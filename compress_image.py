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

    print(s)
    print(v)

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

    return {"S": s, "U": u, "V": v}

def compress_image(image: Image, quality: float) -> Image:
    """Given an image, compress it to a certain quality level given between 0 and 1."""

    # Convert the image to grayscale, then to a numpy matrix
    grayscale_image: Image = image.convert("L")
    image_matrix: np.ndarray = np.array(grayscale_image) # apparently np.matrix is deprecated?

    # Call the singular value decomposition function on the matrix

    # Use quality to determine how many singular values to keep
    
    # Reconstruct the image from the singular values matrix

    # Convert the numpy matrix back to an image

    return image_matrix

test_matrix: np.ndarray = np.array([[2, 0, 1], [0, 2, 0]])
svd: dict = svd(test_matrix)
print(np.matmul(svd["U"], np.matmul(svd["S"], svd["V"].T)))