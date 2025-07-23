# monitor_log.py
import time
import re
from collections import deque, defaultdict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOG_PATH = "/var/log/nginx/access.log"  # ou o caminho correto
MAX_REQUESTS = 100
TIME_WINDOW = 10  # segundos

ip_requests = defaultdict(lambda: deque())

def extract_ip(line):
    match = re.match(r"^(\d+\.\d+\.\d+\.\d+)", line)
    return match.group(1) if match else None

class LogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("access.log"):
            with open(event.src_path, 'r') as f:
                lines = f.readlines()[-20:]  # lê últimas linhas
                now = time.time()
                for line in lines:
                    ip = extract_ip(line)
                    if ip:
                        timestamps = ip_requests[ip]
                        timestamps.append(now)
                        while timestamps and now - timestamps[0] > TIME_WINDOW:
                            timestamps.popleft()
                        if len(timestamps) > MAX_REQUESTS:
                            print(f"[ALERTA] Potencial DDoS de {ip} com {len(timestamps)} requisições em {TIME_WINDOW}s")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(LogHandler(), path=LOG_PATH.rsplit("/", 1)[0], recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
