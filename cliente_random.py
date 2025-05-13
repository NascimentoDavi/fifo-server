import os, random, argparse

parser = argparse.ArgumentParser()
parser.add_argument("operacao", choices=["soma", "sub", "mult", "div"], help="Operação a ser realizada")
args = parser.parse_args()

SERVER_FIFO = "/tmp/rpc_req_fifo"
CLIENT_FIFO = f"/tmp/rpc_resp_{os.getpid()}"

if os.path.exists(CLIENT_FIFO):
    os.remove(CLIENT_FIFO)
os.mkfifo(CLIENT_FIFO, 0o600)

a, b = random.randint(1, 100), random.randint(1, 100)
mensagem = f"{CLIENT_FIFO}|{args.operacao}|{a},{b}\n"

with open(SERVER_FIFO, "w") as server:
    server.write(mensagem)
    server.flush()

with open(CLIENT_FIFO, "r") as resposta:
    print(f"{args.operacao}({a}, {b}) = {resposta.readline().strip()}")
