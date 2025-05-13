import os

SERVER_FIFO = "/tmp/rpc_req_fifo"

if os.path.exists(SERVER_FIFO):
    os.remove(SERVER_FIFO)
os.mkfifo(SERVER_FIFO, 0o600)

def soma(a, b): return a + b
def sub(a, b): return a - b

OPERACOES = {
    "soma": soma,
    "sub": sub
}

print("Servidor RPC iniciado...")

while True:
    with open(SERVER_FIFO, "r") as server:
        linha = server.readline().strip()
        if not linha:
            continue

        try:
            resp_fifo, operacao, parametros = linha.split("|")
            args = list(map(int, parametros.split(",")))
            resultado = OPERACOES[operacao](*args) if operacao in OPERACOES else "Operação inválida"
        except Exception as e:
            resultado = f"Erro: {str(e)}"

        with open(resp_fifo, "w") as cliente:
            cliente.write(str(resultado) + "\n")
            cliente.flush()
