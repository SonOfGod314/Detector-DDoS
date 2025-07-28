# Bloqueio automático via Netsh

import os

def bloquear_ip(ip):
    comando = f'netsh advfirewall firewall add rule name="Bloquear IP {ip}" dir=in action=block remoteip={ip}'
    os.system(comando)
    print(f"[FIREWALL] IP {ip} bloqueado com Netsh.")

