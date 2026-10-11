
import sys, re
try:
    from urllib.request import Request, urlopen
except Exception:
    urlopen = None

EXPECTED_FLAG = "RAVEN{the_implant_knows_you}"


KEY = 0x5A
ENC_CODE = bytes([0x0F,0x09,0x1C,0x1F,0x77,0x13,0x14,0x0C,0x77,0x6A,0x6D])

def recover_code(binary_path):
    
    data = open(binary_path, "rb").read()
    present = ENC_CODE in data
    code = bytes(b ^ KEY for b in ENC_CODE).decode()
    return present, code

def hit_server(base, code):
    
    url = base.rstrip("/") + "/api/v3/register"
    req = Request(url, data=b"", method="POST", headers={
        "X-Raven-ID":   "RAVEN-17",
        "X-GDN-Client": "guardian_update",
        "Authorization": code,
    })
    with urlopen(req, timeout=10) as r:
        return r.read().decode()

def main(binary_path, base):
    print(f"[*] binary: {binary_path}")
    present, code = recover_code(binary_path)
    print(f"[1] ENC_CODE bytes found in binary: {present}")
    print(f"[2] recovered activation code (XOR 0x5A): {code}")

    print(f"[3] replaying recovered creds to {base}/api/v3/register ...")
    try:
        body = hit_server(base, code)
    except Exception as e:
        print(f"    [!] server call failed: {e}")
        print("    (server එක up ද? docker compose up -d --build)")
        sys.exit(1)
    print("    server response:", body)

    m = re.search(r"RAVEN\{[a-z0-9_]+\}", body)
    flag = m.group(0) if m else None
    print(f"[4] flag: {flag}")

    ok = present and code == "USFE-INV-07" and flag == EXPECTED_FLAG
    print("[RESULT] PASS ✔" if ok else "[RESULT] FAIL ✘")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    binp = sys.argv[1] if len(sys.argv) > 1 else "dist/guardian_update.exe"
    base = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8083"
    main(binp, base)
