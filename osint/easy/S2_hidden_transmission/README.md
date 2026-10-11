# S2 — Hidden Transmission  (RAVEN//TRACE)

OSINT / Reconnaissance challenge. The player starts from the attacker
identifier **RAVEN-17** (recovered in S1), correlates across an isolated
"fake internet" (search engine, dev profile, code repo + commits, blog,
WHOIS/cert, web-archive), and recovers a flag hidden in the **oldest**
archived snapshot.

**Flag:** `RAVEN{raven_was_here_first}`
**Delivery:** container-based (nginx serving a static site)
**Consumes:** `RAVEN-17` (from S1)

## The correlation path
```
RAVEN-17  →  ravn17 profile (ex-GuardianOS)  →  watchtower-tools repo
          →  "marker scrubbed in v2"  →  WebVault archive of watchtower-labs.io
          →  EARLIEST snapshot (2026-06-02)  →  flag
```
The current/clean pages have the marker removed. Only the earliest
web-archive capture still contains it — that is the OSINT lesson.

## Pages (the isolated OSINT surface)
| File | Pretends to be |
|------|----------------|
| `index.html` / `results.html` | RavenSearch (search engine) |
| `profile.html` | ravn17 on CodeNest (code host) |
| `repo.html` / `commits.html` | the watchtower-tools repository |
| `blog.html` | ravn17's personal blog |
| `whois.html` | WHOIS / TLS cert lookup |
| `archive.html` + `archive_first/mid/latest.html` | WebVault (web archive) |

All sites, people and data are **fictional / lab-only**.

## Run
```bash
docker compose up -d --build       # then open http://localhost:8082
```

## Verify (author solve / canary)
```bash
python3 solve_S2.py http://localhost:8082     # or:  python3 solve_S2.py ./site
# expect: [RESULT] PASS ✔
```

## Reset
```bash
docker compose down && docker compose up -d --build
```

## Integration contract
- **Input:** `RAVEN-17` — must match what S1 hands the player.
- **Optional seed forward:** the repo references the WATCHTOWER project and
  GuardianOS, reinforcing the lore that pays off in S3/S6. No hard credential
  is passed forward from S2.

> Doc note: the assignment's S2 page writes the validation flag as
> `FLAG{raven_was_here_first}` in one spot, but the Flag field and the Flag
> Register both use `RAVEN{raven_was_here_first}`. This build uses
> **`RAVEN{raven_was_here_first}`** (consistent with the CTF-wide `RAVEN{…}`
> format). Confirm the final string with your team.


