from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

class MistralOCRtoJSON:
    def __init__(self, model_name: str = "mychen76/mistral7b_ocr_to_json_v1"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        bnb_config = BitsAndBytesConfig(
            llm_int8_enable_fp32_cpu_offload=True,
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )

        device_map = {
            "transformer.word_embeddings": 0,
            "transformer.word_embeddings_layernorm": 0,
            "lm_head": 0,
            "transformer.h": 0,
            "transformer.ln_f": 0,
            "model.embed_tokens": 0,
            "model.layers": 0,
            "model.norm": 0    
        }

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16,
            quantization_config=bnb_config,
            device_map=device_map
        )

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    def convert(self, ocr_text: str) -> str:
        prompt = f"""### Instruction:
You are POS receipt data expert, parse, detect, recognize and convert following receipt OCR image result into structure receipt data object. 
Don't make up value not in the Input. Output must be a well-formed JSON object.```json

### Input:
{ocr_text}

### Output:
"""
        self.tokenizer.pad_token = self.tokenizer.eos_token
        with torch.inference_mode():
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, padding=True).to(self.device)
            outputs = self.model.generate(
                input_ids=inputs.input_ids,
                attention_mask=inputs.attention_mask,
                pad_token_id=self.tokenizer.eos_token_id,
                max_new_tokens=8192
            )
            result_text = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        return result_text
