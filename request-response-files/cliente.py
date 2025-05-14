import os

SERVER_FIFO = "/tmp/read_response_fifo/rpc_req_fifo"
CLIENT_FIFO = "f/tmp/read_response_fifo/rpc_resp_{os.getpid()}" # Cada host tem seu PID no próprio FIFO de resposta

# Cria o FIFO e remove se já existir
for fifo in [SERVER_FIFO, CLIENT_FIFO]:
    if os.path.exists(fifo):
        os.remove(fifo)
    os.mkfifo(fifo, mode=0o600)

reply = input("Qual arquivo você precisa?")