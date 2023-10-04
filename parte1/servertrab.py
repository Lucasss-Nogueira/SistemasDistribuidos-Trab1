import socket
import threading

# Lista de clientes conectados
clientes = []
# Lista de apelidos dos clientes
apelidos = []

# Função para enviar mensagens para todos os clientes
def enviar_mensagem(mensagem, cliente):
    for c in clientes:
        if c != cliente:
            c.send(mensagem.encode('utf-8'))

# Função para lidar com a conexão de um cliente
def handle_cliente(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024).decode('utf-8')
            if mensagem.startswith('/ENTRAR'):
                apelido = mensagem.split()[1]
                if apelido not in apelidos and len(clientes) < 4:
                    apelidos.append(apelido)
                    clientes.append(cliente)
                    cliente.send('Conectado ao chat!'.encode('utf-8'))
                    enviar_mensagem(f'{apelido} entrou no chat.', cliente)
                else:
                    #len==4 ? cliente.send('Chat cheio!'.encode('utf-8')): cliente.send('Apelido já em uso.'.encode('utf-8'))
                    if len == 4:
                        cliente.send('Chat cheio!'.encode('utf-8'))
                    else:
                        cliente.send('Apelido já em uso.'.encode('utf-8'))
                    continue
                    ##cliente.close()
            elif cliente in clientes:          
                if mensagem.startswith('/USUARIOS'):
                    cliente.send(', '.join(apelidos).encode('utf-8'))
                elif mensagem.startswith('/NICK'):
                    novo_apelido = mensagem.split()[1]
                    if novo_apelido not in apelidos:
                        antigo_apelido = apelidos[clientes.index(cliente)]
                        apelidos[clientes.index(cliente)] = novo_apelido
                        enviar_mensagem(f'{antigo_apelido} agora é {novo_apelido}.', cliente)
                    else:
                        cliente.send('Apelido já em uso.'.encode('utf-8'))
                elif mensagem.startswith('/SAIR'):
                    indice = clientes.index(cliente)
                    apelido = apelidos[indice]
                    apelidos.pop(indice)
                    clientes.pop(indice)
                    enviar_mensagem(f'{apelido} saiu do chat.', cliente)
                    cliente.close()
                    break
                else:
                    enviar_mensagem(f'{apelidos[clientes.index(cliente)]}: {mensagem}', cliente)
            else:
                cliente.send('Cliente nao logado, sem autorizacao para o comando informado!'.encode('utf-8'))
        except:
            indice = clientes.index(cliente)
            apelido = apelidos[indice]
            apelidos.pop(indice)
            clientes.pop(indice)
            enviar_mensagem(f'{apelido} saiu do chat.', cliente)
            cliente.close()
            break

# Configurações do servidor
host = '127.0.0.1'
porta = 12345

# Inicializa o servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, porta))
servidor.listen()

print('Servidor iniciado...')

# Aceita e lida com as conexões dos clientes
while True:
    cliente, endereco = servidor.accept()
    print(f'Conexão estabelecida com {str(endereco)}')
    thread_cliente = threading.Thread(target=handle_cliente, args=(cliente,))
    thread_cliente.start()