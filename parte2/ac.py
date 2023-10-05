# import socket
# import messages_pb2

# # Configurações do ar-condicionado
# AC_IP = '127.0.0.1'
# AC_PORT = 12345

# # Inicializa o socket do ar-condicionado
# ac_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ac_socket.connect((AC_IP, AC_PORT))

# # Mensagem de identificação do ar-condicionado
# equipamento_info = messages_pb2.EquipmentInfo()
# equipamento_info.type = 'AC'
# equipamento_info.ip = AC_IP
# equipamento_info.port = AC_PORT
# ac_socket.send(equipamento_info.SerializeToString())

# # Lógica do ar-condicionado
# while True:
#     comando = input('Comando para o ar-condicionado (ligar/desligar/temperatura): ')
#     if comando.lower() == 'ligar':
#         comando_msg = messages_pb2.Command(type=messages_pb2.Command.AC, state=True)
#         ac_socket.send(comando_msg.SerializeToString())
#     elif comando.lower() == 'desligar':
#         comando_msg = messages_pb2.Command(type=messages_pb2.Command.AC, state=False)
#         ac_socket.send(comando_msg.SerializeToString())
#     elif comando.lower().startswith('temperatura'):
#         try:
#             temperatura = int(comando.split()[1])
#             comando_msg = messages_pb2.Command(type=messages_pb2.Command.AC, temperature=temperatura)
#             ac_socket.send(comando_msg.SerializeToString())
#         except (IndexError, ValueError):
#             print('Comando de temperatura inválido. Use "temperatura <valor>".')
#     else:
#         print('Comando inválido. Use "ligar", "desligar" ou "temperatura <valor>".')
import socket
import messages_pb2

# Configurações do ar-condicionado
AC_IP = '127.0.0.1'
AC_PORT = 12345
EQUIPAMENTO_TIPO = 'AC'

# Inicializa o socket do ar-condicionado
ac_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ac_socket.connect((AC_IP, AC_PORT))

# Mensagem de identificação do ar-condicionado
equipamento_info = messages_pb2.EquipmentInfo()
equipamento_info.type = EQUIPAMENTO_TIPO
equipamento_info.ip = AC_IP
equipamento_info.port = AC_PORT
ac_socket.send(equipamento_info.SerializeToString())

# Aguarda comandos do Gateway e executa as ações correspondentes
while True:
    comando_msg = ac_socket.recv(1024)
    comando = messages_pb2.Command()
    comando.ParseFromString(comando_msg)

    if comando.type == messages_pb2.Command.AC:
        if comando.state:
            print('Ar-condicionado ligado.')
            # Lógica para ligar o ar-condicionado
        else:
            print('Ar-condicionado desligado.')
            # Lógica para desligar o ar-condicionado
        if comando.HasField('temperature'):
            temperatura = comando.temperature
            print(f'Temperatura definida para: {temperatura}°C')
            # Lógica para ajustar a temperatura do ar-condicionado

