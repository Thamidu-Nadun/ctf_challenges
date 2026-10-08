
import sys, re, base64
from scapy.all import rdpcap, TCP, Raw

EXPECTED_FLAG = "RAVEN{traffic_never_lies}"

def main(path):
    pkts = rdpcap(path)

    
    raven_ports = set()
    for p in pkts:
        if TCP in p and Raw in p:
            data = bytes(p[Raw].load)
            if b"X-Raven-ID: RAVEN-17" in data:
                
                raven_ports.add(p[TCP].dport)   # client->server dport = C2 port
    print(f"[1] RAVEN-17 identifier found on C2 port(s): {sorted(raven_ports)}")

    
    c2_port = sorted(raven_ports)[0]
    cli = b""
    for p in pkts:
        if TCP in p and Raw in p and p[TCP].dport == c2_port:
            cli += bytes(p[Raw].load)

    
    body = cli.split(b"\r\n\r\n")[-1].strip()
    decoded = base64.b64decode(body).decode(errors="replace")
    print("[2] decoded C2 exfil blob:")
    for line in decoded.strip().splitlines():
        print("      " + line)

    
    m = re.search(r"RAVEN\{[a-z0-9_]+\}", decoded)
    flag = m.group(0) if m else None
    print(f"[3] recovered flag: {flag}")

    ok = (flag == EXPECTED_FLAG)
    print("[RESULT] PASS ✔" if ok else "[RESULT] FAIL ✘")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "incident_traffic.pcap"
    main(path)
