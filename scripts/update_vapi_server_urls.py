"""
Update Vapi assistant server URLs for the 3 sport gurus.
Usage:
    python scripts/update_vapi_server_urls.py <CRICKET_ID> <FOOTBALL_ID> <CHESS_ID>

Uses the ngrok URL defined in this script.
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VAPI_PRIVATE_KEY")
if not API_KEY:
    print("[ERROR] VAPI_PRIVATE_KEY not found in environment or .env")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

NGROK_URL = "https://ef5d-103-162-211-98.ngrok-free.app"


def update_server_url(name, assistant_id, endpoint_path):
    if assistant_id.startswith("<"):
        print(f"[SKIP] {name}: assistant ID not configured")
        return

    server_url = f"{NGROK_URL}{endpoint_path}"
    update_data = {"serverUrl": server_url}

    print(f"[SETUP] Updating {name} server URL -> {server_url} ...")
    resp = requests.patch(
        f"https://api.vapi.ai/assistant/{assistant_id}",
        headers=HEADERS,
        json=update_data,
    )

    if resp.status_code in [200, 201]:
        print(f"[OK] {name} updated successfully")
    else:
        print(f"[ERROR] {name}: {resp.status_code}")
        print(resp.text)


def main():
    if len(sys.argv) < 4:
        print("Usage: python scripts/update_vapi_server_urls.py <CRICKET_ID> <FOOTBALL_ID> <CHESS_ID>")
        sys.exit(1)

    cricket_id = sys.argv[1]
    football_id = sys.argv[2]
    chess_id = sys.argv[3]

    update_server_url("Cricket Guru", cricket_id, "/vapi/webhook/cricket")
    update_server_url("Football Guru", football_id, "/vapi/webhook/football")
    update_server_url("Chess Guru", chess_id, "/vapi/webhook/chess")


if __name__ == "__main__":
    main()
