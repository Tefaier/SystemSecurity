import requests
import hmac
import hashlib
import time
import sys

BASE_URL = "https://moodquery.is-course.ru"
ANONYMOUS_KEY_ID = "anonymous"
ANONYMOUS_SECRET = "anonymous"

def sign_request(timestamp: int) -> str:
    """Compute HMAC-SHA256 signature for the given timestamp."""
    mac = hmac.new(ANONYMOUS_SECRET.encode(), str(timestamp).encode(), hashlib.sha256)
    return mac.hexdigest()

def make_action_request(action: str, args: list[str]) -> str:
    """Send a signed POST request to the /action endpoint and return the response text."""
    timestamp = int(time.time())
    signature = sign_request(timestamp)

    params = {
        "key_id": ANONYMOUS_KEY_ID,
        "timestamp": str(timestamp)
    }
    headers = {
        "x-signature": signature
    }
    # The server expects multiple "args" fields in the POST form.
    data = [("args", action)] + [("args", arg) for arg in args]

    try:
        resp = requests.post(f"{BASE_URL}/action", params=params, headers=headers, data=data, timeout=5)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        return f"Request failed: {e}"

def main():
    print("MoodQuery interactive client (anonymous)")
    print("Available actions: whoami, ps, ls <path>, head <path>, md5 <path>, sha1 <path>, sha256 <path>, mount")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input.lower() == "exit":
            break

        parts = user_input.split()
        action = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        response = make_action_request(action, args)
        print(response)

if __name__ == "__main__":
    main()
