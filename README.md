
# 🔐 Projeto: Detecção e Mitigação de Ataques DDoS em Servidores Web

Este projeto tem como objetivo **monitorar tráfego HTTP em tempo real a partir dos logs do Apache** e **detectar possíveis ataques DDoS** com base em:
- Quantidade de requisições por IP por minuto.
- Análise comportamental utilizando Machine Learning.
- Geração de relatórios periódicos em JSON.
- Bloqueio automático de IPs maliciosos via firewall (Netsh no Windows).

---

## 🧠 Tecnologias utilizadas

- Python 3.x
- Análise de logs Apache (`access.log`)
- Machine Learning com `scikit-learn`
- Bloqueio de IPs com `netsh` (Windows)
- Simulação de tráfego com `requests`

---

## 📂 Estrutura de arquivos

```
ddos-detector/
├── main.py # Arquivo principal que executa o monitoramento
├── anomaly_detector.py # Verifica comportamento anômalo
├── firewall.py # Lógica de bloqueio de IPs no Windows usando netsh
├── monitor_log.py # Lê e analisa o arquivo de log do Apache em tempo real
├── report_generator.py # Gera relatórios em formato JSON com os dados coletados
├── scapy_monitor.py # (Opcional) Sniffer com Scapy para tráfego em tempo real
├── traffic_simulator.py # Simula tráfego HTTP para testes locais
├── relatorios/ # Pasta onde os relatórios JSON são salvos
```
---

## ⚙️ Requisitos

1. Python 3 instalado
2. Módulos necessários (instale com pip):

```
pip install -r requirements.txt
```

> Se não tiver `requirements.txt`, use:
> ```
> pip install scikit-learn requests
> ```

3. O servidor Apache deve estar em execução.
4. O caminho para o arquivo de log do Apache deve estar correto (por padrão: `C:\xampp\apache\logs\access.log` no Windows).

---

## 🚀 Como executar

### 1. Abra o terminal do Windows (ou VS Code) **como Administrador**
- No Windows, isso é necessário para que o `netsh` funcione corretamente.

### 2. Execute o monitoramento de ataques:

```
python main.py
```

Você verá mensagens como:

```
[INFO] Monitorando C:\xampp\apache\logs\access.log...
[ALERTA] DDoS detectado de 127.0.0.1 (101 reqs)
[FIREWALL] IP 127.0.0.1 bloqueado com Netsh.
[RELATÓRIO] Salvo como relatorio_2025-07-23_21-33-52.json
```

---

### 3. (Opcional) Simular tráfego de ataque

Em outro terminal, rode:

```
python traffic_simulator.py
```

Isso simula múltiplas requisições para sobrecarregar o servidor e testar o sistema de detecção.

---

## 📊 Relatórios

Os relatórios são salvos automaticamente a cada 30 segundos, com o seguinte padrão de nome:

```
relatorio_YYYY-MM-DD_HH-MM-SS.json
```

Cada relatório contém algo como:

```json
{
  "127.0.0.1": 681,
  "192.168.0.5": 22
}
```

Representando o número de requisições por IP.

---

## ✅ Observações

- O IP `127.0.0.1` é usado apenas para testes (localhost).
- O bloqueio real funciona apenas com privilégios de administrador.
- O sistema pode ser adaptado para funcionar com `iptables` no Linux.

---

## 👨‍💻 Autor

Luís Campos – Projeto acadêmico de Segurança (2025)
