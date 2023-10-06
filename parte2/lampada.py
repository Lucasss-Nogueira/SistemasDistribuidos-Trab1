import socket
import messages_pb2

# Configurações da lâmpada
EQUIPAMENTO_TIPO = messages_pb2.Command.LAMP

# Inicializa o socket TCP da lâmpada
lampada_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

    if equipamento_info.type == messages_pb2.Command.GATEWAY:
        gateway_address = (equipamento_info.ip, equipamento_info.port)
        # Conecta à porta específica do Gateway via TCP
        lampada_socket.connect(gateway_address)
        # Envia o tipo do dispositivo para o Gateway
        lampada_socket.send("LAMP".encode())
        print('Lâmpada conectada ao Gateway.\n')
        multicast_socket.close()
        break

# Aguarda comandos do Gateway e executa as ações correspondentes
while True:
    comando_msg = lampada_socket.recv(1024)
    comando = messages_pb2.Command()
    comando.ParseFromString(comando_msg)

    if comando.type == EQUIPAMENTO_TIPO:
        if comando.state:
            print('Lâmpada ligada.\n')
            comando_msg = messages_pb2.Command()
            comando_msg.mensagem = "Lampada foi ligada"
            comando_msg.type = EQUIPAMENTO_TIPO

            lampada_socket.send(comando_msg.SerializeToString())
            # Lógica para ligar a lâmpada
        else:
            print('Lâmpada desligada.\n')
            comando_msg = messages_pb2.Command()
            comando_msg.mensagem = "Lâmpada foi desligada."
            comando_msg.type = EQUIPAMENTO_TIPO
            lampada_socket.send(comando_msg.SerializeToString())
            # Lógica para desligar a lâmpada
