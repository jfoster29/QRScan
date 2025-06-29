"""
pdf_reader.py

Provides PDF-to-image conversion using PyMuPDF and OpenCV.
"""

from typing import List
import fitz  # PyMuPDF
import numpy as np
import cv2


def pdf_to_images(pdf_path: str) -> List[np.ndarray]:
    """
    Convert each page of a PDF into a BGR OpenCV image (NumPy array).

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        List of page images as NumPy arrays in BGR format.
    """
    images = []
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))  # type: ignore
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
            if pix.n == 4:
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
            elif pix.n == 1:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            images.append(img)
    return images 