from transformers import AutoProcessor, LayoutLMv3ForTokenClassification
import torch
from PIL import Image

class LayoutLMv3InvoiceParser:
    def __init__(self, model_name="jinhybr/OCR-LayoutLMv3-Invoice", device=None):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = LayoutLMv3ForTokenClassification.from_pretrained(model_name).to(device)

    def _convert_box(self, polygon, image_size):
        x_coords = [pt[0] for pt in polygon]
        y_coords = [pt[1] for pt in polygon]
        x0, y0, x1, y1 = min(x_coords), min(y_coords), max(x_coords), max(y_coords)
        width, height = image_size
        return [
            int(1000 * x0 / width),
            int(1000 * y0 / height),
            int(1000 * x1 / width),
            int(1000 * y1 / height)
        ]

    def extract_entities(self, ocr_texts, ocr_boxes, image):
        if not isinstance(image, Image.Image):
            raise ValueError("Image must be a PIL.Image.Image")

        if len(ocr_texts) != len(ocr_boxes):
            print("Text-box length mismatch:", len(ocr_texts), len(ocr_boxes))
            return []

        image_size = image.size
        boxes = [self._convert_box(b, image_size) for b in ocr_boxes]

        encoding = self.processor(
            images=image,
            text=ocr_texts,
            boxes=boxes,
            return_tensors="pt",
            truncation=True,
            padding="max_length"
        )

        encoding = {k: v.to(self.device) for k, v in encoding.items()}
        encoding["bbox"] = encoding["bbox"].long()
        outputs = self.model(**encoding)
        logits = outputs.logits[0]
        predictions = torch.argmax(logits, dim=-1).tolist()
        labels = [self.model.config.id2label[p] for p in predictions]
        entities = []
        word_ids = encoding.word_ids(batch_index=0)
        already_seen = set()
        for idx, word_id in enumerate(word_ids):
            if word_id is None or word_id in already_seen:
                continue
            if labels[idx] != "O":
                entities.append({
                    "text": ocr_texts[word_id],
                    "label": labels[idx]
                })
            already_seen.add(word_id)

        return entities