import os

SERVER_FIFO = "/tmp/read_response_fifo/rpc_req_fifo"
CLIENT_FIFO = f"/tmp/read_response_fifo/rpc_resp_{os.getpid()}" # Cada host tem seu PID no próprio FIFO de resposta

# Cria o FIFO e remove se já existir
for fifo in [SERVER_FIFO, CLIENT_FIFO]:
    if os.path.exists(fifo):
        os.remove(fifo)
    os.mkfifo(fifo, mode=0o600)

# Solicita o nome do arquivo
file = input("Qual arquivo você precisa?")

# Monta a mensagem de requisição no formato: CLIENT_FIFO|nome_do_arquivo
message = f"{CLIENT_FIFO}|{file}"

# Envia a requisicao para o servidor
with open(SERVER_FIFO, "w") as server:
    server.write(message)
    server.flush() # This forces the message to be written immediately, instead of waiting for the buffer to fill

with open(CLIENT_FIFO, "r") as answer:
    print("Files content: ")
    for lines in answer:
        print(lines.strip())

# Remove o FIFO de resposta
os.remove(CLIENT_FIFO)