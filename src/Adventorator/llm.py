# llm.py

import requests
import json

class LLM:
    def __init__(self, model="qwen3:1.7b-q8_0", url="http://localhost:8901/api/chat", api_type="ollama"):
        self.model = model
        self.url = url
        self.api_type = api_type

    def prepare_request_data(self, user_prompt="Hello", think=True, stream=False, temperature=0.7):
        headers = {"Content-Type": "application/json"}
        if not think:
            user_prompt = "/nothink " + user_prompt
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": user_prompt}],
            "stream": stream,
            "options": {"temperature": temperature}
        }
        return self.url, headers, data, user_prompt

# Example usage:
llm = LLM(model="qwen3:1.7b-q8_0", url="http://localhost:8901/api/chat", api_type="ollama")
url, headers, data, user_prompt = llm.prepare_request_data(user_prompt="Tell me about Jupiter.", think=False, stream=False, temperature=0.7)
response = requests.post(url, headers=headers, data=json.dumps(data))