# SistemasDistribuidos-Trab1
Parte 1 e parte 2 do trabalho de Sistemas Distribuídos.

## Para a parte 1:
Foi definido um servidor Chat_TCP, com suporte para 4 usários conectados os quais ele gerencia as mensagens.

### Funcionamento da aplicação:
#### 1. Deve informar o IP e a porta do servidor ao qual deseja se conectar. Além do seu nome de usuário (apelido).
A aplicação cliente automaticamente já irá conectar ao SocketTCP com as informações passadas e além de enviar \ENTRAR (apelido_digitado) para tentar logar no chat, caso o apelido já esteja sendo usado, o servidor irá informar à aplicação cliente, que dessa vez irá necessitar digitar manualmente o comando \ENTRAR (apelido) para logar.
Antes de logar, a aplicação cliente não terá acesso a nenhuma funcionalidade do Chat_TCP.

#### 2. \NICK 
O cliente poderá utilizar este comando para solicitar que o seu nome seja alterado pelo servidor para um novo que não esteja sendo utilizado.

#### 3. \USUARIOS
O cliente poderá utilizar este comando para solicitar que o servidor envie quais usuários estão logados no Chat_TCP.

#### 4. Enviar mensagens
Qualquer mensagem escrita pelo cliente que não começe por "\" será interpretada como uma mensagem a ser enviadas para todos os outros clientes, com a identificação do apelido do usuário que a enviou.

#### 5. \SAIR
 O cliente poderá utilizar esse comando para deslogar do Chat_TCP.

 ### Linguagem utilizada: 
 #### + Python
 ### Bibliotecas utilizadas :
 #### + Socket
 #### + Threading 

 ## Para a parte 2:
 Foi definido um ambiente de casa inteligente, composto por um gateway principal, um AC (sensor contínuo de temperatura), uma lâmpada (capaz de ser ligada e desligada) e uma fechadura eletrônica (que se abre caso seja informada a senha correta), tais dispostivios foram definidos de forma abstrata por meio de software.
 
 ### Funcionamento da aplicação:
 #### 1. 
 Inicialmente, o gateway começa seu processo de descoberta multicast, no qual solicita que os dispositivos encontrados se conectem com o gateway via TCP (por meio das informações passadas pelo gateway no processo de descoberta multicast, o IP e a porta do socket TCP) e se identifiquem. 

 #### 2. 
 Quando os dispostivos conseguem estabelecer a conexão TCP e se identificar, encerram a conexão com o socket UDP utilizado no processo de descoberta/identificação e ficam disponíveis para exercer as suas funcionalidades. Sejam estas receber comandos ou enviar medidas periodicamente. Para o AC, por exemplo, estabelece-se uma nova conexão UDP, que será utilizada para o envio periódico dos seus registros de temperatura e una conexão TCP que será utilizada para o recebimento de comandos.

 #### 3. 
 Por meio da interface de linha de comando embutida no gateway é possível enviar os dispositivos os seus respectivos comandos.
 ##### 3.1. AC - Definir a temperatura:
 \temperatura <valor_da_temperatura> 
 ##### 3.2. Fechadura eletrônica - Liberar a fechadura:
 \senha <senha> 
 ##### 3.3. Lâmpada - Ligar ou desligar a luz:
 \ligar ou \desligar

 ### Definição dos protocolos de comunicação via Protocol Buffers:
 ![Proto](https://github.com/Lucasss-Nogueira/SistemasDistribuidos-Trab1/assets/104247878/b65c7a4d-3cfc-456d-a03b-ea7e702e56cd)

#### Command -
Utilizado para enviar  os comandos. 
+ EquipamentType - Informa o equipamento que enviou o commando.
+ State - Informa o estado da lâmpada.
+ Mensagem - Informa a mensagem a ser passada junta ao comando.
+ Temperatura - Informa a atual temperatura do AC
+ Password - Senha a ser passada junto ao comando da fechadura eletrônica.
#### EquipamentInfo -
Utilizado para enviar informações do dispostivo no momento da descoberta.
+ Type - Tipo do equipamento ( AC, LAMP, GATEWAY, LOCK ).
+ IP - Ip do equipamento.
+ Porta - Porta na qual o equipamento está conectado.
 
 ### Linguagens utilizadas: 
 #### + Python
 #### + Protocol Buffers3
 ### Bibliotecas utilizadas :
 #### + Socket
 #### + Threading 
 #### + Struct
 #### + Timer
 #### + Text
 #### + text_format from google.protobuf


