# Captura de pacotes com Scapy em tempo real

from scapy.all import sniff, IP
from collections import defaultdict, deque
import time

MAX_PACKETS = 100
TIME_WINDOW = 10
packet_history = defaultdict(lambda: deque())

def process_packet(packet):
    if IP in packet:
        ip_src = packet[IP].src
        now = time.time()
        history = packet_history[ip_src]
        history.append(now)
        while history and now - history[0] > TIME_WINDOW:
            history.popleft()
        if len(history) > MAX_PACKETS:
            print(f"[SCAPY ALERTA] {ip_src} enviou {len(history)} pacotes em {TIME_WINDOW}s")

sniff(filter="ip", prn=process_packet)
