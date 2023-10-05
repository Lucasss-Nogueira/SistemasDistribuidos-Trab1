# import socket
# import messages_pb2

# # Configurações da fechadura
# LOCK_IP = '127.0.0.1'
# LOCK_PORT = 12348
# SENHA_CORRETA = '1234'  # Defina sua senha aqui

# # Inicializa o socket da fechadura
# lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# lock_socket.connect((LOCK_IP, LOCK_PORT))

# # Mensagem de identificação da fechadura
# equipamento_info = messages_pb2.EquipmentInfo()
# equipamento_info.type = 'LOCK'
# equipamento_info.ip = LOCK_IP
# equipamento_info.port = LOCK_PORT
# lock_socket.send(equipamento_info.SerializeToString())

# # Lógica da fechadura
# while True:
#     comando_msg = lock_socket.recv(1024)
#     comando = messages_pb2.Command()
#     comando.ParseFromString(comando_msg)
    
#     if comando.type == messages_pb2.Command.LOCK:
#         senha = comando.password
#         if senha == SENHA_CORRETA:
#             print('Fechadura: Porta aberta.')
#         else:
#             print('Fechadura: Senha incorreta. Porta permanece fechada.')
import socket
import messages_pb2

# Configurações da fechadura
LOCK_IP = '127.0.0.1'
LOCK_PORT = 12345
EQUIPAMENTO_TIPO = 'LOCK'

# Inicializa o socket da fechadura
lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lock_socket.connect((LOCK_IP, LOCK_PORT))

# Mensagem de identificação da fechadura
equipamento_info = messages_pb2.EquipmentInfo()
equipamento_info.type = EQUIPAMENTO_TIPO
equipamento_info.ip = LOCK_IP
equipamento_info.port = LOCK_PORT
lock_socket.send(equipamento_info.SerializeToString())

# Aguarda comandos do Gateway e executa as ações correspondentes
while True:
    comando_msg = lock_socket.recv(1024)
    comando = messages_pb2.Command()
    comando.ParseFromString(comando_msg)

    if comando.type == messages_pb2.Command.LOCK:
        senha = comando.password
        print(f'Senha recebida: {senha}')
        # Lógica para verificar a senha e abrir/fechar a porta
