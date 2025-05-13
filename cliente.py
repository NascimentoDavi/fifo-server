import os

SERVER_FIFO = "/tmp/rpc_req_fifo"
CLIENT_FIFO = f"/tmp/rpc_resp_{os.getpid()}"

# Cria os FIFOs (remove se já existir)
for fifo in [SERVER_FIFO, CLIENT_FIFO]:
    if os.path.exists(fifo):
        os.remove(fifo)
    os.mkfifo(fifo, mode=0o600)

# Entrada do usuário
entrada = input("Digite a operação e dois parâmetros (ex: soma 3 5): ")
partes = entrada.strip().split()
operacao = partes[0]
params = ",".join(partes[1:])

mensagem = f"{CLIENT_FIFO}|{operacao}|{params}\n"

# Envia a requisição ao servidor
with open(SERVER_FIFO, "w") as server:
    server.write(mensagem)
    server.flush()

# Aguarda e lê a resposta
with open(CLIENT_FIFO, "r") as resposta:
    print("Resultado:", resposta.readline().strip())
