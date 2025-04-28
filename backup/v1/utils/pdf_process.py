import fitz  # PyMuPDF
import numpy as np
import cv2

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