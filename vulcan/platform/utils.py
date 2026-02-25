import hashlib

import requests


def generate_vulcan_agent_id(url: str, api_key: str) -> str:
    raw = f"{url}:{api_key}"
    return hashlib.sha256(raw.encode()).hexdigest()[:12]


def parse_vulcan_id(id: str) -> str:
    return id.split("-")[-1]


def get_agent_card(url: str, api_key: str) -> str:
    response = requests.get(
        f"{url}/.well-known/agent-card.json",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    print(response.json())
    return str(response.json())


def send_a2a_request(url: str, api_key: str, prompt: str) -> str:
    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        json={
            "jsonrpc": "2.0",
            "id": "req-1",
            "method": "message/send",
            "params": {
                "message": {
                    "id": "123456",
                    "messageId": "123456",
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            },
        },
    )
    print(response.json())
    return str(response.json())
