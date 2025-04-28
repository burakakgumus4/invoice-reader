import re

def extract_items_from_texts(texts):
    items = []
    current_item = {}
    for text in texts:
        text_clean = text.strip()
        if re.match(r"^PRD-\d{3,6}$", text_clean):
            if current_item:
                items.append(current_item)
                current_item = {}
            current_item["sku"] = text_clean

        elif "description" not in current_item and not any(k in text_clean.lower() for k in ["qty", "price", "total", "po", "invoice"]):
            current_item["description"] = text_clean

        elif match := re.match(r"^Qty[:\s]*(\d+)", text_clean, re.IGNORECASE):
            current_item["quantity"] = int(match.group(1))

        elif match := re.match(r"^Price[:\s]*\$?([\d.,]+)", text_clean, re.IGNORECASE):
            current_item["unit_price"] = float(match.group(1).replace(",", ""))

        elif match := re.match(r"^Total[:\s]*\$?([\d.,]+)", text_clean, re.IGNORECASE):
            current_item["total_price"] = float(match.group(1).replace(",", ""))

    if current_item:
        items.append(current_item)

    return items