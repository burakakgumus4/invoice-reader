from transformers import AutoProcessor, LayoutLMv3ForTokenClassification
import torch
from PIL import Image

class BertPOExtractor:
    def __init__(self, model_name="jinhybr/OCR-LayoutLMv3-Invoice", device="cpu"):
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = LayoutLMv3ForTokenClassification.from_pretrained(model_name)
        self.model.to(device)
        self.device = device

    def extract_po(self, ocr_texts, ocr_boxes, image):
        words = ocr_texts
        boxes = [[int(x) for x in box] for box in ocr_boxes]
        encoded_inputs = self.processor(
            image=Image.fromarray(image),
            words=words,
            boxes=boxes,
            return_tensors="pt",
            truncation=True,
            padding="max_length"
        )
        for k in encoded_inputs:
            encoded_inputs[k] = encoded_inputs[k].to(self.device)
        outputs = self.model(**encoded_inputs)
        predictions = torch.argmax(outputs.logits, dim=-1).squeeze().tolist()
        labels = [self.model.config.id2label[p] for p in predictions]
        po_candidates = [word for word, label in zip(words, labels) if "PO" in label.upper()]
        return list(set(po_candidates))