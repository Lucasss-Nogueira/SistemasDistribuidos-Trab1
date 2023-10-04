import socket
import threading

# Função para receber mensagens do servidor
def receber_mensagens():
    while True:
        try:
            mensagem = cliente.recv(1024).decode('utf-8')
            print(mensagem)
        except:
            print('Erro ao receber mensagens.')
            cliente.close()
            break

# Configurações do cliente
host = input('Digite o IP do servidor: ')
porta = int(input('Digite a porta do servidor: '))
apelido = input('Digite seu apelido: ')

# Conecta ao servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, porta))

# Envia o comando /ENTRAR com o apelido escolhido
cliente.send(f'/ENTRAR {apelido}'.encode('utf-8'))

# Inicia a thread para receber mensagens
thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.start()

# Envia mensagens para o servidor
while True:
    mensagem = input()
    cliente.send(mensagem.encode('utf-8'))