import time
from collections import defaultdict, deque
from firewall import bloquear_ip
from report_generator import gerar_relatorio_json
from anomaly_detector import AnomalyDetector
import threading
import os
import re

# Configurações
LOG_PATH = "C:\\xampp\\apache\\logs\\access.log" # caminho do log do Apache
MAX_REQUESTS = 100
TIME_WINDOW = 10  # (segundos)
BLOQUEAR_IP = True
GERAR_RELATORIO = True

# Armazenamento de timestamps por IP
ip_reqs = defaultdict(lambda: deque())
ip_contador = defaultdict(int)

# Expressão regular para extrair IP
def extrair_ip(linha):
    match = re.search(r"((\d{1,3}\.){3}\d{1,3}|::1)", linha)
    return match.group(1) if match else None

# Monitoramento em tempo real do log
def monitorar_log():
    print(f"[INFO] Monitorando {LOG_PATH}...")
    with open(LOG_PATH, 'r') as log:
        log.seek(0, os.SEEK_END) 
        while True:
            linha = log.readline()
            if not linha:
                time.sleep(0.1)
                continue

            agora = time.time()
            ip = extrair_ip(linha)
            if ip:
                timestamps = ip_reqs[ip]
                timestamps.append(agora)
                ip_contador[ip] += 1

                while timestamps and agora - timestamps[0] > TIME_WINDOW:
                    timestamps.popleft()

                if len(timestamps) > MAX_REQUESTS:
                    print(f"[ALERTA] DDoS detectado de {ip} ({len(timestamps)} reqs)")
                    if BLOQUEAR_IP:
                        bloquear_ip(ip)
                    timestamps.clear()  # evita múltiplos alertas seguidos

# Treinamento e detecção anômala periódica
def detectar_anomalias():
    while True:
        if ip_contador:
            # Coleta de dados
            dados = list(ip_contador.values())
            ips = list(ip_contador.keys())

            # Treinamento do modelo com os dados coletados
            detector = AnomalyDetector()
            detector.treinar(dados)

            # Detectcao de anomalias
            resultados = detector.detectar(dados)

            print("\n[ML] Verificação anômala:")
            for ip, count, resultado in zip(ips, dados, resultados):
                status = "ANOMALIA" if resultado == -1 else "NORMAL"
                print(f"{ip}: {count} reqs -> {status}")
        time.sleep(30)


# Relatório periódico
def gerar_relatorio_periodico():
    while True:
        print("[DEBUG] IPs registrados até agora:", dict(ip_contador))
        if GERAR_RELATORIO:
            gerar_relatorio_json(dict(ip_contador))
        time.sleep(10)
    
# Execução dos módulos em paralelo
if __name__ == "__main__":
    t1 = threading.Thread(target=monitorar_log)
    t2 = threading.Thread(target=detectar_anomalias)
    t3 = threading.Thread(target=gerar_relatorio_periodico)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
