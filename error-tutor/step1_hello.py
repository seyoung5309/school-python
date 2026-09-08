import requests

MODEL = "qwen2.5-coder:3b"
URL = "http://localhost:11434/api/chat"

def ask(prompt):
    res = requests.post(URL, json={
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }, timeout=180)
    res.raise_for_status()
    return res.json()["message"]["content"]

print(ask("디자인 패턴이란 무엇인가?"))
# print(ask("파이썬에서 IndexError 가 나는 이유를 한 문장으로 설명해줘."))