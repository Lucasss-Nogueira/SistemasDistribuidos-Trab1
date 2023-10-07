import socket
import struct
import threading
import messages_pb2
import time
from google.protobuf import text_format
# Dicionário para armazenar informações sobre os equipamentos conectados
equipamentos = {}

# Função para lidar com a conexão de um cliente
def handle_cliente(cliente_socket, endereco):
    while True:
        comando_msg = cliente_socket.recv(1024)
        comando = messages_pb2.Command()
        comando.ParseFromString(comando_msg)
        
        # if comando.type in equipamentos:
        #     equipamento_socket = equipamentos[comando.type]
        #     equipamento_socket.send(comando_msg)
        # else:
        #     print(f'Equipamento desconhecido: {comando.type}')

        if len(comando.mensagem) > 3:
            print(f'Mensagem recebida de {comando.EquipmentType.Name(comando.type)}: \n{comando.mensagem}\n')

        if comando.type == messages_pb2.EquipmentInfo.AC:
            temperatura = comando.temperature
            print(f'Temperatura recebida do AC: {temperatura}°C')

# Função para descoberta multicast
def multicast_discovery():
    multicast_group = '224.0.0.1'
    multicast_port = 10001

    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    multicast_socket.bind(('', 0))

    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print('Gateway: Enviando mensagem de descoberta...')
    descoberta_msg = messages_pb2.EquipmentInfo()
    descoberta_msg.type = messages_pb2.EquipmentInfo.GATEWAY  # Define o tipo como GATEWAY
    descoberta_msg.ip = socket.gethostbyname(socket.gethostname())  # IP do Gateway
    descoberta_msg.port = 12345  # Porta do Gateway

    while True:
        multicast_socket.sendto(descoberta_msg.SerializeToString(), (multicast_group, multicast_port))
        time.sleep(1)  # Envia a mensagem de descoberta a cada segundo

# Função para enviar comandos para os equipamentos


def enviar_comando():
    while True:

        tipo = input('Digite o tipo do equipamento (LAMP, AC, LOCK): \n')
        if tipo in equipamentos:
            
            comando_msg = messages_pb2.Command()
            print(comando_msg)
            state = False
            temperatura = 0
            senha = "pass" 
            comando_msg.type = tipo
            comando_msg.temperature = temperatura
            comando_msg.state = state
            comando_msg.password = senha

            if tipo == 'LAMP':
                comando = input('Digite o comando (ligar/desligar): \n')
                if comando.lower() == 'desligar':
                    state = False
                elif comando.lower() == 'ligar':
                    state = True
                else:
                    print('Comando inválido.\n')
                    continue

            elif tipo == 'AC':
                comando = input('Digite o comando (temperatura): \n')
                # if comando.lower().startswith('temperatura'):
                    # try:
                if (comando.isnumeric()):
                    temperatura = int(comando)
                else:
                    print('Comando inválido.\n')
                    continue
                    
                    # except (IndexError, ValueError):
                    #     print('Comando de temperatura inválido. Use "temperatura <valor>".')
                    #     continue
                # else:
                #     print('Comando inválido.')
                #     continue

            elif tipo == 'LOCK':
                comando = input('Digite o comando (senha): \n')
                if comando.lower().startswith('senha'):
                    senha = comando.split()[1]
                    state = ~state
                else:
                    print('Comando inválido.\n')
                    continue

            
            comando_msg.state = state
            comando_msg.password = senha
            comando_msg.temperature = temperatura
            equipamento_socket = equipamentos[tipo]
            equipamento_socket.send(comando_msg.SerializeToString())

        else:
            print(f'Equipamento desconhecido: {tipo}\n')

# Configurações do Gateway
HOST =  socket.gethostbyname(socket.gethostname()) #'127.0.0.1'
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

# Inicializa o socket UDP como None (ainda não criado)
udp_socket = None
print('Gateway iniciado...\n')

# Aceita e lida com as conexões dos clientes
while True:
    cliente_socket, endereco = server_socket.accept()
    # recebe tipo de dispositivo e faz o decode
    comando_msg = cliente_socket.recv(1024)
    comando = messages_pb2.Command()
    comando.ParseFromString(comando_msg)

    tipo_dispositivo = comando.EquipmentType.Name(comando.type)  # tipo do dispositivo
    equipamentos[tipo_dispositivo] = cliente_socket
    print(f'Conexão estabelecida com {str(endereco)} (Tipo de dispositivo: {tipo_dispositivo})')
    
    if tipo_dispositivo == 'AC' and udp_socket is None:
        # Se o dispositivo for o ar-condicionado e o socket UDP ainda não foi criado
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((HOST, 12346))  # Porta para receber temperatura
        print('Socket UDP para temperatura criado.')
        
        # Inicia a thread para lidar com a recepção de temperatura
        thread_cliente = threading.Thread(target=handle_cliente, args=(udp_socket, endereco))
        thread_cliente.start()
    thread_cliente = threading.Thread(target=handle_cliente, args=(cliente_socket, endereco))
    thread_cliente.start()
