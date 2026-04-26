"""
Start ngrok tunnel and update Vapi assistant server URLs.
Usage:
    python scripts/update_vapi_server_urls.py

Prerequisites:
    - ngrok installed and authenticated (ngrok authtoken <TOKEN>)
    - .env file with VAPI_PRIVATE_KEY
    - Docker containers running (backend on port 8001)
"""

import os
import sys
import json
import time
import subprocess
from urllib.request import urlopen, Request
from urllib.error import URLError

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

BACKEND_PORT = 8001

CERT_ID = "ec398ab7-64e2-47f6-abe7-f4752ca51b9e"
TAX_ID = "a4696f51-15e8-4556-aa7e-3901edb806dd"
GRIEVANCE_ID = "fd34e6be-5a44-4a15-b1a4-4b1f39fc7d0f"

ASSISTANTS = [
    ("Birth & Death Certificates", CERT_ID, "/vapi/webhook/certificates"),
    ("Property Tax", TAX_ID, "/vapi/webhook/tax"),
    ("Public Grievance", GRIEVANCE_ID, "/vapi/webhook/grievances"),
]


def get_ngrok_url(retries=15, delay=2):
    print("[NGROK] Checking for existing tunnel ...")
    for _ in range(retries):
        try:
            req = Request("http://127.0.0.1:4040/api/tunnels")
            with urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode())
            tunnels = data.get("tunnels", [])
            if tunnels:
                public_url = tunnels[0]["public_url"]
                print(f"[NGROK] Found active tunnel: {public_url}")
                return public_url
        except (URLError, ConnectionError, OSError):
            pass
        time.sleep(delay)
    return None


def start_ngrok():
    print(f"[NGROK] Starting tunnel to localhost:{BACKEND_PORT} ...")
    subprocess.Popen(
        ["ngrok", "http", str(BACKEND_PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
    )
    time.sleep(3)
    return get_ngrok_url(retries=15, delay=2)


def update_server_url(name, assistant_id, ngrok_url, endpoint_path):
    server_url = f"{ngrok_url}{endpoint_path}"
    update_data = {"serverUrl": server_url}

    print(f"[VAPI] Updating {name} -> {server_url} ...")
    resp = requests.patch(
        f"https://api.vapi.ai/assistant/{assistant_id}",
        headers=HEADERS,
        json=update_data,
    )

    if resp.status_code in [200, 201]:
        print(f"[VAPI] OK: {name} updated")
    else:
        print(f"[VAPI] ERROR: {name}: {resp.status_code}")
        print(resp.text[:300])


def main():
    ngrok_url = get_ngrok_url()

    if not ngrok_url:
        print("[NGROK] No active tunnel found. Starting new one ...")
        ngrok_url = start_ngrok()

    if not ngrok_url:
        print("[ERROR] Could not start ngrok tunnel. Make sure ngrok is installed and authenticated.")
        sys.exit(1)

    print()
    print(f"{'='*60}")
    print(f"  NGROK PUBLIC URL: {ngrok_url}")
    print(f"{'='*60}")
    print()

    for name, assistant_id, endpoint_path in ASSISTANTS:
        update_server_url(name, assistant_id, ngrok_url, endpoint_path)

    print()
    print(f"[DONE] All assistants updated.")
    print()
    print(f"[INFO] Webhook endpoints:")
    for name, _, endpoint_path in ASSISTANTS:
        print(f"  {ngrok_url}{endpoint_path}  ({name})")


if __name__ == "__main__":
    main()
