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

