# import socket
# import messages_pb2

# # Configurações da lâmpada
# LAMP_IP = '127.0.0.1'
# LAMP_PORT = 12345

# # Inicializa o socket da lâmpada
# lamp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# lamp_socket.connect((LAMP_IP, LAMP_PORT))

# # Mensagem de identificação da lâmpada
# equipamento_info = messages_pb2.EquipmentInfo()
# equipamento_info.type = 'LAMP'
# equipamento_info.ip = LAMP_IP
# equipamento_info.port = LAMP_PORT
# lamp_socket.send(equipamento_info.SerializeToString())

# # Lógica da lâmpada
# while True:
#     comando = input('Comando para a lâmpada (ligar/desligar): ')
#     if comando.lower() == 'ligar':
#         comando_msg = messages_pb2.Command(type=messages_pb2.Command.LAMP, state=True)
#         lamp_socket.send(comando_msg.SerializeToString())
#     elif comando.lower() == 'desligar':
#         comando_msg = messages_pb2.Command(type=messages_pb2.Command.LAMP, state=False)
#         lamp_socket.send(comando_msg.SerializeToString())
#     else:
#         print('Comando inválido. Use "ligar" ou "desligar".')
import socket
import messages_pb2

# Configurações da lâmpada
LAMP_IP = '127.0.0.1'
LAMP_PORT = 12345
EQUIPAMENTO_TIPO = 'LAMP'

# Inicializa o socket da lâmpada
lamp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lamp_socket.connect((LAMP_IP, LAMP_PORT))

# Mensagem de identificação da lâmpada
equipamento_info = messages_pb2.EquipmentInfo()
equipamento_info.type = EQUIPAMENTO_TIPO
equipamento_info.ip = LAMP_IP
equipamento_info.port = LAMP_PORT
lamp_socket.send(equipamento_info.SerializeToString())

# Aguarda comandos do Gateway e executa as ações correspondentes
while True:
    comando_msg = lamp_socket.recv(1024)
    comando = messages_pb2.Command()
    comando.ParseFromString(comando_msg)

    if comando.type == messages_pb2.Command.LAMP:
        if comando.state:
            print('Lâmpada ligada.')
            # Lógica para ligar a lâmpada
        else:
            print('Lâmpada desligada.')
            # Lógica para desligar a lâmpada

