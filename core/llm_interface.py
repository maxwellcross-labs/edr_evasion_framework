import requests
import json
import time
from typing import Optional, Dict, List

class LLMInterface:
    def __init__(self, api_endpoint: str, api_key: str, model: str = "gpt-4o"):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.model = model
        self.max_retries = 3
        self.timeout = 30

    def generate_payload_variation(self, 
                                   objective: str, 
                                   constraints: Optional[Dict] = None,
                                   style_guidance: Optional[str] = None) -> str:
        prompt = self._build_payload_prompt(objective, constraints, style_guidance)
        for attempt in range(self.max_retries):
            try:
                response = self._call_llm_api(prompt)
                code = self._extract_code_from_response(response)
                if self._validate_generated_code(code):
                    return code
                else:
                    print(f"[!] Generated code failed validation, retrying...")
            except Exception as e:
                print(f"[!] Generation attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
        raise Exception("Failed to generate valid payload after all retries")

    def _build_payload_prompt(self, objective: str, constraints: Optional[Dict], style_guidance: Optional[str]) -> str:
        prompt = f"""Generate a Python script that accomplishes the following objective:

OBJECTIVE: {objective}

REQUIREMENTS:
- Use Windows API calls via ctypes
- Implement proper error handling
- Include realistic timing delays
- Avoid obvious malicious patterns
- Generate syntactically unique implementation

"""
        if constraints:
            prompt += "\nCONSTRAINTS:\n"
            for key, value in constraints.items():
                prompt += f"- {key}: {value}\n"
        if style_guidance:
            prompt += f"\nSTYLE GUIDANCE:\n{style_guidance}\n"
        prompt += """
OUTPUT FORMAT:
Provide only the Python code without explanations or markdown formatting.
The code should be complete and executable.
"""
        return prompt

    def _call_llm_api(self, prompt: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert Python developer specializing in Windows internals and red team tooling."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.9,
            "max_tokens": 3000
        }
        response = requests.post(self.api_endpoint, headers=headers, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

    def _extract_code_from_response(self, response: str) -> str:
        if "```python" in response:
            code = response.split("```python")[1].split("```")[0]
        elif "```" in response:
            code = response.split("```")[1].split("```")[0]
        else:
            code = response
        return code.strip()

    def _validate_generated_code(self, code: str) -> bool:
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError:
            return False