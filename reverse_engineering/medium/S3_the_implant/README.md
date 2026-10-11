# S3 — THE IMPLANT  (RAVEN//TRACE)

Reverse-Engineering challenge. The player reverses `guardian_update.exe`
to recover an XOR-obfuscated activation code (`USFE-INV-07`) plus the
service endpoint and header names, then replays those to a register
server to get the flag.

**Flag:** `RAVEN{the_implant_knows_you}`
**Delivery:** hybrid — downloadable binary (`guardian_update.exe`) + container (register server)
**Consumes:** `RAVEN-17` (S1/S2 tie-in)
**Seeds forward (to S6):** `POST /api/v3/register`, `X-Raven-ID: RAVEN-17`,
`X-GDN-Client: guardian_update`, `Authorization: USFE-INV-07`

> Note on the binary: this is a **benign crackme-style** RE target — a
> local activation-code validator. It has **no networking, no payload,
> no persistence** — it only decodes an embedded value and checks input.
> The RE skill taught (decompile → find the XOR routine → deobfuscate →
> recover the value) is identical to any real malware-config extraction,
> without shipping anything that behaves like malware.

## What the player recovers
| Value | How it's stored | Recover by |
|-------|-----------------|-----------|
| `USFE-INV-07` (activation code / Authorization) | **XOR-encoded** (key 0x5A) | decompile the XOR loop, or run under a debugger and read the decoded buffer |
| `/api/v3/register`, `guardian_update`, `RAVEN-17` | plaintext strings | `strings`, or Ghidra |

## Build (authors)
```bash
sudo apt install -y gcc gcc-mingw-w64-x86-64-win32   # ELF + PE toolchains
./build.sh                 # -> dist/guardian_update.exe  (ship this)
                           #    dist/guardian_update_linux (local test only)
```

## Run the server
```bash
docker compose up -d --build        # POST http://localhost:8083/api/v3/register
```

## Verify (author solve / canary)
```bash
python3 solve_S3.py dist/guardian_update.exe http://localhost:8083
# expect: [RESULT] PASS ✔   (recovers USFE-INV-07, replays, gets the flag)
```

## Player path
1. Open `guardian_update.exe` in Ghidra / radare2 (or run under a debugger).
2. `strings` gives the endpoint + `guardian_update` + `RAVEN-17`, but **not**
   the activation code.
3. Find the `decode()` routine → the encoded byte array + key `0x5A` →
   XOR-decode → `USFE-INV-07`. (Or: run it, break after `decode`, read the buffer.)
4. `curl -X POST http://<host>:8083/api/v3/register -H 'X-Raven-ID: RAVEN-17'
   -H 'X-GDN-Client: guardian_update' -H 'Authorization: USFE-INV-07'` → flag.

## Packaging
- **Binary:** upload `dist/guardian_update.exe` as a challenge file. **Do NOT
  ship `src/` or `dist/guardian_update_linux`** — those give the answer away.
- **Server:** `docker build -t YOURUSER/raventrace-s3-register:1.0 server/`,
  push to Docker Hub, platform exposes port 8080.

## Integration contract
The endpoint + 3 headers here are the **same** values S6 expects. Confirm
with the S6 owner (you) that `USFE-INV-07`, `guardian_update`, `RAVEN-17`,
`/api/v3/register` match S6's C2 register check exactly.


