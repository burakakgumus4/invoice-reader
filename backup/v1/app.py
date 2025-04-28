import os
import json
from models.paddle_ocr import Paddle
from utils.pdf_process import convert_pdf_bytes_to_images
from utils.po_extractor import extract_po_number, extract_supplier_name
from utils.item_extractor import extract_items_from_texts
from utils.validation import validate_items

def process_invoice_from_bytes(pdf_bytes):
    images = convert_pdf_bytes_to_images(pdf_bytes)
    ocr_engine = Paddle()
    results = []

    for i, frame in enumerate(images):
        frame, ocr_results = ocr_engine.perform_ocr(frame, visualize=False)
        texts = ocr_results.texts
        po_number = extract_po_number(texts)
        supplier = extract_supplier_name(texts)
        items = extract_items_from_texts(texts)
        inconsistencies = validate_items(items)

        page_data = {
            "page": i + 1,
            "po_number": po_number,
            "supplier": supplier,
            "items": items,
            "validation_errors": inconsistencies
        }

        results.append(page_data)

    return results

if __name__ == "__main__":
    with open("demo/Invoice_2.pdf", "rb") as f:
        pdf_bytes = f.read()

    data = process_invoice_from_bytes(pdf_bytes)

    os.makedirs("output", exist_ok=True)
    with open("output/structured_output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Data successfully written to output/structured_output.json")
