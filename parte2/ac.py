import socket
import messages_pb2
import time
import threading
# Configurações do ar-condicionado
EQUIPAMENTO_TIPO = messages_pb2.EquipmentInfo.AC
temperatura = 25

# Inicializa o socket TCP do ar-condicionado
ac_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Inicializa o socket de descoberta multicast
multicast_group = '224.0.0.1'
multicast_port = 10001
multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
multicast_socket.bind(('', multicast_port))
multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_group) + socket.inet_aton('0.0.0.0'))

# Inicializa o socket UDP para enviar a temperatura
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_temp_addr = None
while True:
    mensagem, endereco = multicast_socket.recvfrom(1024)
    equipamento_info = messages_pb2.EquipmentInfo()
    equipamento_info.ParseFromString(mensagem)

    if equipamento_info.type == messages_pb2.EquipmentInfo.GATEWAY:
        gateway_address = (equipamento_info.ip, equipamento_info.port)
        udp_temp_addr = (equipamento_info.ip, equipamento_info.port + 1)
        # Conecta à porta específica do Gateway via TCP
        ac_socket.connect(gateway_address)

        # Envia o tipo do dispositivo para o Gateway
        comando_msg = messages_pb2.Command()
        comando_msg.type = EQUIPAMENTO_TIPO
        ac_socket.send(comando_msg.SerializeToString())
        #ac_socket.send("AC".encode()

        print('Ar-condicionado conectado ao Gateway.\n')
        multicast_socket.close()
        break

def enviar_temperatura(ac_socket):
    while True:
        comando_msg = messages_pb2.Command()
        comando_msg.type = EQUIPAMENTO_TIPO
        comando_msg.temperature = temperatura

        udp_socket.sendto(comando_msg.SerializeToString(), udp_temp_addr)
        #ac_socket.send(comando_msg.SerializeToString())
        print(f'Temperatura enviada: {temperatura}°C\n')
        time.sleep(15)
# Thread para enviar a temperatura periodicamente
thread_temperatura = threading.Thread(target=enviar_temperatura, args=(ac_socket,))
thread_temperatura.start()

# Aguarda comandos do Gateway e executa as ações correspondentes
while True:
    comando_msg = ac_socket.recv(1024)
    comando = messages_pb2.Command()
    comando.ParseFromString(comando_msg)
    print(comando)

    if comando.type == EQUIPAMENTO_TIPO:
        # if comando.state:
        #     print('Ar-condicionado ligado.')
        #     # Lógica para ligar o ar-condicionado
        # else:
        #     print('Ar-condicionado desligado.')
        #     # Lógica para desligar o ar-condicionado
        #    if comando.HasField('temperature') and comando.temperature != 0:
        temperatura = comando.temperature
        print(f'Temperatura definida para: {temperatura}°C')
        # Lógica para ajustar a temperatura do ar-condicionado
