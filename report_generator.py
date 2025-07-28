# Relatório JSON

import json
import os
from datetime import datetime

os.makedirs("relatorios", exist_ok=True)

def gerar_relatorio_json(ip_counts):
    if not ip_counts:
        print("[RELATÓRIO] Nenhum IP registrado até o momento. Relatório não gerado.")
        return

    agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join("relatorios", f"relatorio_{agora}.json")
    with open(filename, "w") as f:
        json.dump(ip_counts, f, indent=2)
    print(f"[RELATÓRIO] Salvo como {filename}")