import socket
import struct
import threading
import messages_pb2

# Dicionário para armazenar informações sobre os equipamentos conectados
equipamentos = {}

# Função para lidar com a conexão de um cliente
def handle_cliente(cliente_socket, endereco):
    while True:
        comando_msg = cliente_socket.recv(1024)
        comando = messages_pb2.Command()
        comando.ParseFromString(comando_msg)
        
        if comando.type in equipamentos:
            equipamento_socket = equipamentos[comando.type]
            equipamento_socket.send(comando_msg)
        else:
            print(f'Equipamento desconhecido: {comando.type}')

# Função para descoberta multicast
def multicast_discovery():
    multicast_group = '224.0.0.1'
    multicast_port = 10000
    
    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    multicast_socket.bind(('', multicast_port))
    
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    print('Gateway: Esperando por equipamentos...')
    while True:
        equipamento_ip, _ = multicast_socket.recvfrom(16)
        tipo = equipamento_ip.decode('utf-8')
        equipamento_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        equipamento_socket.connect((tipo, 12345))  # Porta do equipamento
        equipamentos[tipo] = equipamento_socket

        print(f"Gateway: Equipamento encontrado em {equipamento_ip.decode('utf-8')}")

# Função para enviar comandos para os equipamentos
def enviar_comando():
    while True:
        tipo = input('Digite o tipo do equipamento (LAMP, AC, LOCK): ')
        if tipo in equipamentos:
            comando = input('Digite o comando (ligar/desligar/temperatura/senha): ')
            comando_msg = messages_pb2.Command()
            comando_msg.type = tipo

            if comando.lower() == 'ligar':
                comando_msg.state = True
            elif comando.lower() == 'desligar':
                comando_msg.state = False
            elif comando.lower().startswith('temperatura'):
                try:
                    temperatura = int(comando.split()[1])
                    comando_msg.temperature = temperatura
                except (IndexError, ValueError):
                    print('Comando de temperatura inválido. Use "temperatura <valor>".')
                    continue
            elif comando.lower().startswith('senha'):
                senha = comando.split()[1]
                comando_msg.password = senha
            else:
                print('Comando inválido.')
                continue

            equipamento_socket = equipamentos[tipo]
            equipamento_socket.send(comando_msg.SerializeToString())
        else:
            print(f'Equipamento desconhecido: {tipo}')

# Configurações do Gateway
HOST = '127.0.0.1'
PORT = 12345

# Inicializa o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

# Inicia thread para descoberta multicast
thread_multicast = threading.Thread(target=multicast_discovery)
thread_multicast.start()

# Inicia thread para enviar comandos
thread_comandos = threading.Thread(target=enviar_comando)
thread_comandos.start()

print('Gateway iniciado...')

# Aceita e lida com as conexões dos clientes
while True:
    cliente_socket, endereco = server_socket.accept()
    print(f'Conexão estabelecida com {str(endereco)}')
    thread_cliente = threading.Thread(target=handle_cliente, args=(cliente_socket, endereco))
    thread_cliente.start()
