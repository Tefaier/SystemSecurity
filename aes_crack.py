import base64
import os
import re
import urllib.request

b64 = lambda x: base64.urlsafe_b64encode(x).decode()

CHECKPOINT = "flag_progress.bin"


def extract_ct(data):
    """Extract hex ciphertext from response"""
    if isinstance(data, bytes):
        data = data.decode()

    for line in data.split('\n'):
        if 'Output:' in line:
            match = re.search(r'([0-9a-fA-F]{100,})', line)
            if match:
                return match.group(1)
    raise Exception("Failed with " + data)


def send(req):
    """Send request and get hex ciphertext"""
    body = urllib.parse.urlencode({"userinput": req}).encode()
    r = urllib.request.Request(
        "https://aes.is-course.ru/",
        data=body,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    success = False
    for _ in range(5):
        try:
            with urllib.request.urlopen(r, timeout=5) as resp:
                body = resp.read().decode()
                success = True
                break
        except Exception:
            pass
    if not success:
        raise RuntimeError(f"All attempts failed at {req}")
    return extract_ct(body)


def main():
    BLOCK = 16

    if os.path.exists(CHECKPOINT):
        recovered = open(CHECKPOINT, "rb").read()
        print(f"Resuming ({len(recovered)} bytes): {recovered!r}")
    else:
        recovered = b""

    while True:
        filler = b'A' * ((BLOCK - 1) - (len(recovered) % BLOCK))

        hex_extracted = send(b64(filler))
        ct = bytes.fromhex(hex_extracted)
        idx = len(filler) // BLOCK
        target = ct[idx*BLOCK : (idx+1)*BLOCK]

        for b in range(256):
            guess = filler + recovered + bytes([b])
            ct_g = bytes.fromhex(send(b64(guess)))
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