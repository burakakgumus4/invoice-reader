# Invoice Extraction Project

## Project Purpose

This project aims to build a **fully working OCR + ML system** that can extract structured data from **financial documents (invoices)**.
It dynamically processes **varying layouts** and extracts **PO numbers, line items (quantity, unit price, total price), and supplier information**.
The output is delivered in **structured JSON format** along with basic **data validation reports**.

---

## Project Structure

```
├── app.py                 # FastAPI backend
├── index.html             # Frontend upload page
├── static/                # Static files (CSS)
├── templates/             # Jinja2 templates
├── models/                # Different model approaches (BERT extractor, Claude, Mistral, Donut, Paddle OCR)
├── utils/                 # Utility functions (PDF processing etc.)
├── libs/                  # Paddle OCR DLL dependencies (for local Windows support)
├── demo/                  # Provided sample invoices
├── output/                # Saved structured JSON outputs
├── api_key.txt            # Claude API key (not included in GitHub)
├── requirements.txt       # Python package dependencies
└── README.md              # You are here
```

---

## How It Works

1. **Upload a PDF or Image:** via simple drag-and-drop UI
2. **OCR Step:** Extract text and layout information with **PaddleOCR**.
3. **Extraction Step:** Use **Claude 3.5 Sonnet LLM** to dynamically interpret OCR results and generate JSON.
4. **Validation Step:** Basic PO matching and Price Consistency Score are calculated.
5. **Result:** Instant structured JSON is returned to the web page.

---

## Example Output

```json
{
  "supplier": "ABC Corporation",
  "po_numbers": ["PO-123456"],
  "items": [
    {
      "product_code": "PRD-001",
      "description": "Semiconductor Part",
      "quantity": 100,
      "unit_price": 10.50,
      "total_price": 1050.00
    }
  ],
  "validation_score": {
    "po_accuracy": "OK",
    "price_accuracy": "99.5%"
  }
}
```

---

## Requirements

Install requirements with:

```bash
pip install -r requirements.txt
```

If you want to use **GPU version** of PaddleOCR:

```bash
pip install -r requirements-gpu.txt
```

---

## Local Run

```bash
python app.py
```

Then open your browser: http://127.0.0.1:8000

---

## Models Supported

| Model                          | Purpose                       | Notes                     |
| ------------------------------ | ----------------------------- | ------------------------- |
| PaddleOCR                      | Text Detection & OCR          | Local Inference           |
| Claude 3.5 Sonnet              | LLM for Smart JSON Extraction | Requires API Key          |
| Mistral Model (Optional)       | OCR-to-JSON approach          | Available for experiments |
| Donut (Vision-Encoder Decoder) | Alternative Full Model        | Not activated by default  |

---

## Important Notes

- `api_key.txt` must contain your Claude API Key. (NOT committed to GitHub)
- `libs/` folder holds necessary DLLs for PaddleOCR on Windows (if required).

---

## Result

✅ Successfully extracted structured invoice data from 3 complex real-world invoices.
✅ Designed fully modular and extendable pipeline for future model testing.
✅ High JSON extraction accuracy without hardcoded templates.

---

## Special Thanks

Developed by Burak Akgümüş for the assessment project.
