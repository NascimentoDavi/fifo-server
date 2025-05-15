import os


SERVER_FIFO = "/tmp/read_response_fifo/rpc_req_fifo"


# Cria o FIFO de servidor, se nao existir
if not os.path.exists(SERVER_FIFO):
    os.mkfifo(SERVER_FIFO, 0o600)

print("Server is waiting for requests")


# Sempre escutando
while True:
    # Abre o FIFO para leitura
    with open(SERVER_FIFO, "r") as server:
        for request in server:
            request = request.strip()
            if not request:
                continue

            try:
                client_fifo, file_name = request.split("|", 1)
                print(f"Request received: {file_name} to {client_fifo}")


                # Tenta ler o conteudo do arquivo solicitado
                try:
                    with open(file_name, "r") as file:
                        content = file.readlines()
                except FileNotFoundError:
                    content = [f"Erro: arquivo '{file_name}' não encontrado.\n"]
                except Exception as e:
                    content = [f"Error while opening the file :{str(e)}\n"]

                
                # Envia o retorno para o FIFO do cliente
                with open("CLIENT_FIFO", "w") as response:
                    for line in content:
                        response.write(line)
                    response.flush()
                    print(f"Content sent to {client_fifo}")


            except Exception as e:
                print(f"Error while processing request: {str(e)}")