import os
import re
import urllib.parse
import urllib.request
import urllib.error
import time

CHECKPOINT = "flag_progress.bin"


def extract_ct(data):
    """Extract hex ciphertext from response"""
    if isinstance(data, bytes):
        data = data.decode()

    for line in data.split('\n'):
        if 'Output:' in line:
            match = re.search(r'([0-9a-fA-F]{20,})', line)
            if match:
                return match.group(1)
    raise Exception("Failed with " + data)


def send(req):
    """Send the plaintext candidate and get the hex ciphertext."""
    body = urllib.parse.urlencode({"userinput": req}).encode()
    request = urllib.request.Request(
        "https://aes.is-course.ru/",
        data=body,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                return extract_ct(response.read().decode())
        except urllib.error.HTTPError as exc:
            print(f"HTTP {exc.code}; retrying...")
        except Exception as exc:
            print(f"{type(exc).__name__}: {exc}; retrying...")
        time.sleep(1.0 + attempt)

    raise RuntimeError(f"All attempts failed at {req!r}")


def main():
    BLOCK = 16

    if os.path.exists(CHECKPOINT):
        recovered = open(CHECKPOINT, "rb").read()[:-9]
        print(f"Resuming ({len(recovered)} bytes): {recovered!r}")
    else:
        recovered = b""

    while True:
        filler = b'A' * ((BLOCK - 1) - (len(recovered) % BLOCK))
        hex_extracted = send(filler)
        ct = bytes.fromhex(hex_extracted)
        idx = len(recovered) // BLOCK
        target = ct[idx*BLOCK : (idx+1)*BLOCK]

        for b in range(256):
            guess = filler + recovered + bytes([b])
            ct_g = bytes.fromhex(send(guess))
            if ct_g[idx*BLOCK : (idx+1)*BLOCK] == target:
                recovered += bytes([b])
                open(CHECKPOINT, "wb").write(recovered)
                print(recovered)
                break
        else:
            print("Finished without detecting matching byte")
            break

        if recovered.endswith(b'}'):
            break


if __name__ == "__main__":
    main()
