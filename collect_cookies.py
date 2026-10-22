#!/usr/bin/env python3
"""Collect repeated cookies from the pillar challenge login."""
import base64, binascii, json, time
from datetime import datetime, timezone
from pathlib import Path
import requests

URL = "https://pillar.is-course.ru/login"
LOGIN_BODY = "login=test&password=test"
ATTEMPTS = 100
OUTPUT = Path("pillar-cookies.json")

def decoded_base64_hex(value):
    try:
        padded = value + "=" * (-len(value) % 4)
        return base64.b64decode(padded, validate=True).hex()
    except (ValueError, binascii.Error):
        return None

records = []
for attempt in range(ATTEMPTS):
    with requests.Session() as session:
        response = session.post(
            URL,
            data=LOGIN_BODY,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.6.2 Safari/605.1.15",
                "Referer": "https://pillar.is-course.ru/",
            },
            allow_redirects=True,
            timeout=15,
        )
        response.raise_for_status()
        cookies = []
        for cookie in session.cookies:
            cookies.append({
                "name": cookie.name,
                "value": cookie.value,
                "base64_decoded_hex": decoded_base64_hex(cookie.value),
                "domain": cookie.domain,
                "path": cookie.path,
            })
        records.append({
            "attempt": attempt + 1,
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "status": response.status_code,
            "final_url": response.url,
            "cookies": cookies,
        })
        print(f"attempt {attempt + 1}: {[c['name'] for c in cookies]}")
    time.sleep(0.5)

OUTPUT.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
print(f"saved {len(records)} attempts to {OUTPUT}")
