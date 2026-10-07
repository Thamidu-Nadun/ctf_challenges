# S1 — The Traffic  (RAVEN//TRACE)

Network Traffic Analysis challenge. Players analyse a packet capture,
follow the suspicious C2 stream, recover the attacker identifier
**RAVEN-17** (carried into S2) and the flag.

**Flag:** `RAVEN{traffic_never_lies}`
**Delivery:** downloadable file (`incident_traffic.pcap`)

## Build
```bash
pip install scapy
python3 make_pcap.py        # -> incident_traffic.pcap
```

## Verify (author solve / canary)
```bash
python3 solve_S1.py incident_traffic.pcap   # expect: [RESULT] PASS
```

## Player path
Open pcap in Wireshark → Statistics ▸ Conversations → spot the odd
stream to `45.133.9.17:8080` carrying `X-Raven-ID: RAVEN-17` →
Follow HTTP/TCP Stream → base64-decode the POST body → flag.


