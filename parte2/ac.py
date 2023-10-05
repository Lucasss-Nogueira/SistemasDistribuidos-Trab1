import socket
import messages_pb2

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

while True:
    mensagem, endereco = multicast_socket.recvfrom(1024)
    equipamento_info = messages_pb2.EquipmentInfo()
    equipamento_info.ParseFromString(mensagem)

    if equipamento_info.type == messages_pb2.EquipmentInfo.GATEWAY:
        gateway_address = (equipamento_info.ip, equipamento_info.port)
        # Conecta à porta específica do Gateway via TCP
        ac_socket.connect(gateway_address)
        # Envia o tipo do dispositivo para o Gateway
        ac_socket.send("AC".encode())
        print('Ar-condicionado conectado ao Gateway.')
        multicast_socket.close()
        break

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
