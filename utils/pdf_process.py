import fitz
import numpy as np
import cv2
import os

def load_all_pdf_bytes_from_directory(directory_path: str) -> dict:
    pdf_dict = {}
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            try:
                pdf_dict[filename] = load_pdf_bytes(file_path)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return pdf_dict


def load_pdf_bytes(file_path: str) -> bytes:
    if not file_path.lower().endswith(".pdf"):
        raise ValueError(f"Unsupported file format: {file_path}")
    with open(file_path, "rb") as f:
        return f.read()

def convert_pdf_bytes_to_images(pdf_bytes, zoom=2):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []
    for page in doc:
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        if pix.n == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)

        else:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            
        images.append(img)

    return images

def structure_pdf_images(pdfs: dict) -> dict:
    structured = {}
    for filename, pdf_bytes in pdfs.items():
        images = convert_pdf_bytes_to_images(pdf_bytes)
        structured[filename] = {
            "filename": filename,
            "num_pages": len(images),
            "pages": images
        }
    return structured