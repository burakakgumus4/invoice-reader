import requests
import json

class ClaudeParser:
    def __init__(self, api_key, model="claude-3-5-sonnet-20241022", api_url="https://api.anthropic.com/v1/messages"):
        self.api_key = api_key
        self.model = model
        self.api_url = api_url
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

    def _build_prompt(self, texts):
        joined_text = "\n".join(texts)
        prompt = f"""You are an invoice parsing expert.
                    Here is the OCR extracted text from an invoice:
                    ---
                    {joined_text}
                    ---
                    Task: Parse this text into a clean and properly structured JSON object.
                    Do NOT add any explanation. ONLY return a clean JSON.
                """
        return prompt

    def ask(self, texts, max_tokens=4096):
        prompt = self._build_prompt(texts)

        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"Claude API request failed: {response.status_code} - {response.text}")

        completion = response.json()["content"][0]["text"]
        try:
            parsed_json = json.loads(completion)
            return parsed_json
        except json.JSONDecodeError:
            print("Warning: Claude returned invalid JSON.")
            return completion
