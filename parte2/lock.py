import socket
import messages_pb2
from google.protobuf import text_format
# Configurações da fechadura
EQUIPAMENTO_TIPO = messages_pb2.EquipmentInfo.LOCK
senha_correta = "1234"
estado_fechadura = False  # Inicialmente fechada

# Inicializa o socket TCP da fechadura
fechadura_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        fechadura_socket.connect(gateway_address)
        # Envia o tipo do dispositivo para o Gateway
        comando_msg = messages_pb2.Command()
        comando_msg.type = EQUIPAMENTO_TIPO
        fechadura_socket.send(comando_msg.SerializeToString())
        #fechadura_socket.send("LOCK".encode())
        print('Fechadura conectada ao Gateway.\n')
        multicast_socket.close()
        break

# Aguarda comandos do Gateway e executa as ações correspondentes
while True:
    comando_msg = fechadura_socket.recv(1024)
    comando = messages_pb2.Command()
    comando.ParseFromString(comando_msg)

    if comando.type == EQUIPAMENTO_TIPO:

        if comando.password == senha_correta:
            estado_fechadura = comando.state

            if estado_fechadura:
                comando_msg = messages_pb2.Command()
                comando_msg.type = EQUIPAMENTO_TIPO
                comando_msg.mensagem = "Fechadura foi aberta"
                print('Fechadura aberta.\n')
                fechadura_socket.send(comando_msg.SerializeToString())
            else:
                print('Fechadura fechada.\n')
                comando_msg = messages_pb2.Command()
                comando_msg.type = EQUIPAMENTO_TIPO                
                comando_msg.mensagem = "Fechadura fechada."
                fechadura_socket.send(comando_msg.SerializeToString())
        else:
            comando_msg = messages_pb2.Command()
            comando_msg.type = EQUIPAMENTO_TIPO            
            print('Senha incorreta. Fechadura permanece no estado atual.\n')
            comando_msg.mensagem = "Senha incorreta. Fechadura permanece no estado atual."
            fechadura_socket.send(comando_msg.SerializeToString())
