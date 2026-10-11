# S6 — WATCHTOWER  (RAVEN//TRACE capstone)

Multi-domain capstone. Player SSHes into a foothold (S5 creds), speaks
to the C2 as the implant (S1/S2/S3 artifacts), is handed a pivot path,
hops through a gateway into a **segmented monitoring network**, and
reads the WATCHTOWER evidence package.

**Flag:** `RAVEN{you_were_the_attacker}`
**Delivery:** container-based (Docker Hub images / this compose stack)

## Topology (3 segmented networks)
```
player ──ssh:2222──> foothold ─┐ (edge+core)
                               ├─ c2            (core only)
                               └─ watchtower-gw (core+mon)  ──> watchtower (mon only)
```
`watchtower` is reachable **only** via `watchtower-gw`. The player
cannot touch it directly — that is the pivot.

## Run
```bash
docker compose up -d --build
```

## Verify (author solve / canary)
```bash
sudo apt install -y sshpass
./solve_S6.sh               # expect: [RESULT] PASS
```

## Reset
```bash
docker compose down && docker compose up -d --build
```

## Integration contract (coordinate with your team)
`.env` holds the values the player must have recovered from S1–S5:
RAVEN-17 (S1/S2), USFE-INV-07 + guardian_update (S3),
j.portal:Bl4ck0ut!2026 + WATCHTOWER_API_KEY (S5).
Confirm these exact strings match what the other stages hand out.


