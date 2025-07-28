# Simulador de tráfego com pico de um IP malicioso

import requests
import time

URL = "http://127.0.0.1"
while True:
    try:
        requests.get(URL)
        time.sleep(0.05)  # intervalos de 50ms
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar requisição: {e}")
        break
