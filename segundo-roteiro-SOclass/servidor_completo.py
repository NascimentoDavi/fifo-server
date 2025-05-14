# servidor.py
import os

SERVER_FIFO = "/tmp/rpc_req_fifo"

if os.path.exists(SERVER_FIFO):
    os.remove(SERVER_FIFO)
os.mkfifo(SERVER_FIFO, 0o600)

def soma(a, b): return a + b
def sub(a, b): return a - b
def mult(a, b): return a * b
def div(a, b): return a / b if b != 0 else "Erro: divisão por zero"

OPERACOES = {
    "soma": soma,
    "sub": sub,
    "mult": mult,
    "div": div
}   

print("Servidor RPC com múltiplas operações iniciado...")

while True:
    with open(SERVER_FIFO, "r") as server:
        for linha in server:
            linha = linha.strip()
            if not linha:
                continue

            try:
                resp_fifo, operacao, parametros = linha.split("|")
                args = list(map(int, parametros.split(",")))
                resultado = OPERACOES[operacao](*args) if operacao in OPERACOES else "Operação inválida"
            except Exception as e:
                resultado = f"Erro: {str(e)}"

            # Espera o cliente abrir o FIFO antes de escrever
            try:
                with open(resp_fifo, "w") as cliente:
                    cliente.write(str(resultado) + "\n")
            except Exception as e:
                print(f"Erro ao responder: {e}")
