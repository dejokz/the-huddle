"""
Update Vapi assistant system prompts for all squad members.
Usage:
    python scripts/update_vapi_prompts.py

Requires VAPI_PRIVATE_KEY in environment.
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VAPI_PRIVATE_KEY")
if not API_KEY:
    print("[ERROR] VAPI_PRIVATE_KEY not found in environment")
    exit(1)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# Current ngrok URL for reference
NGROK_URL = "https://ef5d-103-162-211-98.ngrok-free.app"

# Map assistant names to their IDs and prompt files
ASSISTANTS = {
    "Huddle Host": {
        "id": "<HOST_ASSISTANT_ID>",
        "prompt_file": "vapi-squad/huddle-host-prompt.md",
        "model": "gpt-5.4",
    },
    "Cricket Guru": {
        "id": "<CRICKET_ASSISTANT_ID>",
        "prompt_file": "vapi-squad/cricket-guru-prompt.md",
        "model": "gpt-5.4",
    },
    "Football Guru": {
        "id": "<FOOTBALL_ASSISTANT_ID>",
        "prompt_file": "vapi-squad/football-guru-prompt.md",
        "model": "gpt-5.4",
    },
    "Chess Guru": {
        "id": "<CHESS_ASSISTANT_ID>",
        "prompt_file": "vapi-squad/chess-guru-prompt.md",
        "model": "gpt-5.4",
    },
}


def update_assistant(name, config):
    assistant_id = config["id"]
    if assistant_id.startswith("<"):
        print(f"[SKIP] {name}: assistant ID not configured")
        return

    prompt_path = Path(config["prompt_file"])
    if not prompt_path.exists():
        print(f"[SKIP] {name}: prompt file not found at {prompt_path}")
        return

    system_prompt = prompt_path.read_text(encoding="utf-8")

    update_data = {
        "model": {
            "provider": "openai",
            "model": config["model"],
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                }
            ],
        }
    }

    resp = requests.patch(
        f"https://api.vapi.ai/assistant/{assistant_id}",
        headers=HEADERS,
        json=update_data,
    )

    if resp.status_code in [200, 201]:
        print(f"[OK] {name} updated ({len(system_prompt)} chars)")
    else:
        print(f"[ERROR] {name}: {resp.status_code}")
        print(resp.text)


def main():
    for name, config in ASSISTANTS.items():
        update_assistant(name, config)


if __name__ == "__main__":
    main()
