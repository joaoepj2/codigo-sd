# IPC Monitor — Painel Rich com Sockets

Painel de monitoramento de comunicação entre processos em tempo real.

## Arquitetura

```
workers.py  ──TCP:5555──►  broker.py  ──TCP:5556──►  monitor.py
(5 workers)                (roteador)                (painel Rich)
```

## Instalação

```bash
pip install rich
```

## Como rodar (3 terminais)

```bash
# Terminal 1 — broker (inicie primeiro)
python broker.py

# Terminal 2 — workers
python workers.py

# Terminal 3 — painel
python monitor.py
```

## O que o painel mostra

| Seção          | Conteúdo                                              |
|----------------|-------------------------------------------------------|
| Resumo         | Total de workers, online, mensagens, erros, % sucesso |
| Processos      | Status, endereço, contadores e barra de saúde por worker |
| Log            | Últimas mensagens em tempo real com tipo e payload    |
| Alertas        | Erros recentes e workers que ficaram offline          |

## Personalizações rápidas

- `MAX_LOG_VISIBLE` em `monitor.py` — número de linhas do log visíveis
- `REFRESH_HZ` em `monitor.py` — frequência de atualização (padrão: 4/s)
- `MAX_LOG` em `broker.py` — tamanho do histórico no broker
- Adicione workers em `workers.py` na lista `configuracoes`

## Integrar com seu próprio processo

Qualquer processo pode conectar ao broker enviando JSON via TCP:

```python
import socket, json

def enviar(worker_id, tipo, payload):
    with socket.create_connection(("127.0.0.1", 5555)) as s:
        msg = {"worker_id": worker_id, "type": tipo, "payload": payload}
        s.sendall((json.dumps(msg) + "\n").encode())

enviar("meu-processo", "task", "processando arquivo X")
enviar("meu-processo", "error", "timeout na leitura")
```

Tipos suportados: `task`, `result`, `error` (qualquer string funciona).
