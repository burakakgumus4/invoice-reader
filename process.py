import os
import fitz
import cv2
import numpy as np
from PIL import Image
from models.paddle_ocr import Paddle
from models.claude import ClaudeParser



def load_api_key(file_path="api_key.txt"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"API key file '{file_path}' not found.")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()
    
def process_invoice_from_bytes(file_bytes):
    images = []

    try:
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        for page in pdf:
            pix = page.get_pixmap()
            img = cv2.imdecode(np.frombuffer(pix.tobytes("png"), np.uint8), cv2.IMREAD_COLOR)
            images.append(img)
    except Exception:
        img = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
        images.append(img)

    all_texts = []
    for img in images:
        _, ocr_result = paddle.perform_ocr(img, visualize=False, class_format=True)
        all_texts.extend(ocr_result.texts)

    result_json = claude.ask(all_texts)

    return result_json


paddle = Paddle()
api_key = load_api_key()
claude = ClaudeParser(api_key=api_key)










