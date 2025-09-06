"""
test ollama chat nostream

example json result:
{
    'model': 'qwen3:1.7b-q8_0', 
    'created_at': '2025-09-06T01:54:30.1595919Z', 
    'message': {
        'role': 'assistant', 
        'content': '<think>\nOkay, the user said "Hello" in the query. I need to respond appropriately. Let me start by acknowledging their greeting. I should keep it friendly and open-ended to encourage further conversation. Maybe add a bit of enthusiasm to make it sound natural. I should also offer help in case they have any questions or need assistance. Let me check the tone to make sure it\'s welcoming and not too formal. Alright, that should cover it.\n</think>\n\nHello! How can I assist you today? 😊'
    }, 
    'done_reason': 'stop', 
    'done': True, 
    'total_duration': 2662046300, 
    'load_duration': 1928924900, 
    'prompt_eval_count': 9, 
    'prompt_eval_duration': 142621400, 
    'eval_count': 105, 
    'eval_duration': 588998000
}

"""

import requests
import json

def prepare_request_data(think=True):
    url = "http://localhost:8901/api/chat"
    headers = {"Content-Type": "application/json"}
    user_content = "Tell me about Jupiter."
    if not think:
        user_content = "/nothink " + user_content
    data = {
        "model": "qwen3:1.7b-q8_0",
        "messages": [{"role": "user", "content": user_content}],
        "stream": False
    }
    return url, headers, data, user_content

# Example usage:
url, headers, data, user_content = prepare_request_data(think=False)

# response will be of type dict
response = requests.post(url, headers=headers, data=json.dumps(data))
#print(response.json())

# Validate the response structure
assert isinstance(response.json(), dict)

# Check if the response contains the expected keys
expected_keys = ["model", "created_at", "message", "done_reason", "done", "total_duration", "load_duration", "prompt_eval_count", "prompt_eval_duration", "eval_count", "eval_duration"]
for key in expected_keys:
    assert key in response.json(), f"Missing key: {key}"

# print the user prompt
print("\nuser prompt: \n", user_content)

# print the 'thinking' content
print("\nthinking: \n", response.json().get("message", {}).get("content", "").split("<think>")[1].split("</think>")[0].strip())

# print the message content after the '</think>' tag
print("\nmessage: \n", response.json().get("message", {}).get("content", "").split("</think>")[1].strip())