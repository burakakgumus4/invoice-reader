from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch
import numpy as np
import cv2

class DonutInvoiceParser:
    def __init__(self, model_name="mychen76/invoice-and-receipts_donut_v1"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = DonutProcessor.from_pretrained(model_name)
        self.model = VisionEncoderDecoderModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

    def _ensure_pil_image(self, image_input):
        if isinstance(image_input, Image.Image):
            return image_input.convert("RGB")
        elif isinstance(image_input, np.ndarray):
            return Image.fromarray(cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB)).convert("RGB")
        else:
            raise ValueError("Unsupported image input type")

    def parse(self, image_input):
        image = self._ensure_pil_image(image_input)
        pixel_values = self.processor(image, return_tensors="pt").pixel_values.to(self.device)
        task_prompt = "<s_receipt>"
        decoder_input_ids = self.processor.tokenizer(task_prompt, return_tensors="pt").input_ids.to(self.device)

        outputs = self.model.generate(
            pixel_values,
            decoder_input_ids=decoder_input_ids,
            max_length=512,
            pad_token_id=self.processor.tokenizer.pad_token_id,
            eos_token_id=self.processor.tokenizer.eos_token_id,
        )

        result = self.processor.batch_decode(outputs, skip_special_tokens=True)[0]
        return result
