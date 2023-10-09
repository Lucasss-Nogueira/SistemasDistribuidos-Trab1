# SistemasDistribuidos-Trab1
Parte 1 e parte 2 do trabalho de Sistemas Distribuídos -

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

 ### Linguagem utlizada: 
 #### . Python
 ### Bibliotecas utilizadas :
 #### . Socket
 #### . Threading 

 ## Para a parte 2:
 Foi definido um ambiente de casa inteligente, composto por um gateway principal, um AC (sensor contínuo de temperatura), uma lâmpada (capaz de ser ligada e desligada) e uma fechadura eletrônica (que se abre caso seja informada a senha correta).
 
 ### Funcionamento da aplicação:
 #### 1. Inicialmente, o gateway começa seu processo de descoberta multicast, no qual solicita que os dispositivos encontrados se conectem com o gateway via TCP (por meio das informações passadas pelo gateway no processo de descoberta multicast, o IP e a porta do socket TCP) e se identifiquem. 

 #### 2. Quando os dispostivos conseguem estabelecer a conexão TCP e se identificar, encerram a conexão com o socket UDP utilizado no processo de descoberta/identificação e ficam disponíveis para exercer as suas funcionalidades. Sejam estas receber comandos ou enviar medidas periodicamente. Para o AC, por exemplo, estabelece-se uma nova conexão UDP, que será utilizada para o envio periódico dos seus registros de temperatura e una conexão TCP que será utilizada para o recebimento de comandos.

 ### Linguagem utlizada: 
 #### . Python
 #### . Protocol Buffers3
 ### Bibliotecas utilizadas :
 #### . Socket
 #### . Threading 


