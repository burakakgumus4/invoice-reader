import re

def extract_po_number(texts):
    """
    Finds potential PO numbers from OCR'd text using regex patterns.
    """
    po_patterns = [
        r"\bPO[-\s:]?\d{3,10}\b",        
        r"\bPurchase Order[:\s]*\d+\b",  
        r"#PO[_-]?\d+"                  
    ]
    
    for text in texts:
        for pattern in po_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group()
    return None


def extract_supplier_name(texts):
    blacklist_keywords = ["TOTAL", "SUBTOTAL", "AMOUNT", "$", "VAT", "INVOICE"]
    for text in texts[:8]:
        clean_text = text.upper()
        if any(keyword in clean_text for keyword in blacklist_keywords):
            continue

        if text.isupper() and len(text.split()) >= 2:
            return text.strip()

    return None
