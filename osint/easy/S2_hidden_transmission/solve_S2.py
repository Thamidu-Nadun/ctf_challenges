
import sys, re, os
from collections import deque
try:
    from urllib.request import urlopen
    from urllib.parse import urljoin
except Exception:
    urlopen = None

EXPECTED_FLAG = "RAVEN{raven_was_here_first}"
FLAG_RE = re.compile(r"RAVEN\{[a-z0-9_]+\}")
LINK_RE = re.compile(r'href="([^"#?]+\.html)(?:[^"]*)?"')

def fetch(base, page):
    
    if base.startswith("http"):
        with urlopen(base.rstrip("/") + "/" + page, timeout=10) as r:
            return r.read().decode("utf-8", "replace")
    with open(os.path.join(base, page), encoding="utf-8") as f:
        return f.read()

def crawl(base, start="index.html"):
    
    seen, q, found_on = set(), deque([start]), {}
    while q:
        page = q.popleft()
        if page in seen:
            continue
        seen.add(page)
        try:
            html = fetch(base, page)
        except Exception as e:
            print(f"    [skip] {page}: {e}")
            continue
        if FLAG_RE.search(html):
            found_on[page] = FLAG_RE.search(html).group(0)
        for link in LINK_RE.findall(html):
            link = link.split("/")[-1]
            if link.endswith(".html") and link not in seen:
                q.append(link)
    return seen, found_on

def main(base):
    print(f"[*] crawling OSINT surface from: {base}")
    seen, found = crawl(base)
    print(f"[1] reachable pages ({len(seen)}): " + ", ".join(sorted(seen)))

    
    if not found:
        print("[RESULT] FAIL ✘  — no flag reachable"); sys.exit(1)
    print("[2] flag found on:")
    for pg, fl in found.items():
        print(f"      {pg}  ->  {fl}")

    
    flag = next(iter(found.values()))
    correct_page = "archive_first.html" in found

    
    clean = [p for p in ("repo.html","archive_latest.html","archive_mid.html") if p in found]

    print(f"[3] flag value: {flag}")
    print(f"[4] flag is on the EARLIEST snapshot (archive_first.html): {correct_page}")
    print(f"[5] flag absent from current/clean pages: {not clean}  "
          f"{'(leaked on: '+', '.join(clean)+')' if clean else ''}")

    ok = (flag == EXPECTED_FLAG) and correct_page and not clean
    print("[RESULT] PASS ✔" if ok else "[RESULT] FAIL ✘")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "./site"
    main(base)
