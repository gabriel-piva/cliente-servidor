# Importando as bibliotecas necessárias
import socket, os, sys

# Imprime mensagens vermelhas
def print_error(message):
    print('\033[91m' + message + '\033[0m')

# Verifica se o número de argumentos está correto
if len(sys.argv) != 2:
    print_error("Uso: python3 script_name.py server_name")
    exit(1)

# Obtém o nome do servidor a partir do argumento fornecido
serverName = sys.argv[1]

# Definindo o nome do servidor e a porta
# serverName = 'localhost'
serverPort = 12000

# Criando um objeto de soquete TCP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conecta o socket ao endereço do servidor e porta
clientSocket.connect((serverName, serverPort))

while True:
    # Solicita ao usuário uma sentença
    sentence = input('\033[1;33m$:\033[0m ')
    message = ''

    cmd = sentence.split()[0]

    if cmd == 'pwd':
        # Envia a sentença codificada para o servidor através do socket
        clientSocket.send(sentence.encode())
        clientSocket.recv(1024)

        # Recebe a resposta do servidor, com tamanho máximo de 1024 bytes
        modifiedSentence = clientSocket.recv(1024)
        message = modifiedSentence.decode()
        clientSocket.send('ACK'.encode())

    elif cmd == 'ls':
        # Envia a sentença codificada para o servidor através do socket
        clientSocket.send(sentence.encode())
        clientSocket.recv(1024)

        # Recebe a resposta do servidor, com tamanho máximo de 1024 bytes
        modifiedSentence = clientSocket.recv(1024)
        message = modifiedSentence.decode()
        clientSocket.send('ACK'.encode())

    elif cmd == 'cd':
        # Envia a sentença codificada para o servidor através do socket
        clientSocket.send(sentence.encode())
        clientSocket.recv(1024)

        # Recebe a resposta do servidor, com tamanho máximo de 1024 bytes
        modifiedSentence = clientSocket.recv(1024)
        message = modifiedSentence.decode()
        clientSocket.send('ACK'.encode())

    # O comando exit fecha o cliente
    elif cmd == 'exit':
        # Envia a sentença codificada para o servidor através do socket
        clientSocket.send(sentence.encode())
        clientSocket.recv(1024)
        #clientSocket.close()
        break

    elif cmd == 'scp': 
        # Envia a sentença codificada para o servidor através do socket
        clientSocket.send(sentence.encode())
        clientSocket.recv(1024)

        # Veirifica se o arquivo existe ou foi encontrado
        file_found = clientSocket.recv(1024)
        clientSocket.send('ACK1'.encode())
        if file_found.decode() == '1':
            # Separando o nome do arquivo do caminho dele
            args = sentence.strip().split()[1]
            file_name = os.path.basename(args)
            
            # Recebendo o tamanho do arquivo
            file_size = clientSocket.recv(1024)
            clientSocket.send('ACK2'.encode())
            file_size = int(file_size.decode())
            
            # Tamanho máximo do pacote
            max_packet_size = 1400
            
            # Recebendo os dados do arquivo do servidor
            file = open(file_name, 'wb')
            while file_size > 0:
                # Se o tamanho do arquivo for maior que o limite do pacote
                # será recebido o a quantidade de dados max do pacote 
                if(file_size > max_packet_size):
                    file_data = clientSocket.recv(max_packet_size)
                    file.write(file_data)
                    clientSocket.send('ACK3'.encode())
                    file_size -= max_packet_size
                # Se não, será recebido o tamanho que falta
                else:
                    file_data = clientSocket.recv(file_size)
                    file.write(file_data)
                    clientSocket.send('ACK4'.encode())
                    file_size -= file_size
            file.close()
            print('Chegou mais rápido que o SEDEX')  

            # Recebe a resposta do servidor, com tamanho máximo de 1024 bytes
            modifiedSentence = clientSocket.recv(1024)
            message = modifiedSentence.decode()
            clientSocket.send('ACK5'.encode())
        else:
            # Recebe a resposta do servidor, com tamanho máximo de 1024 bytes
            modifiedSentence = clientSocket.recv(1024)
            message = modifiedSentence.decode()
            clientSocket.send('ACK6'.encode())  
    else:
        print('Comando inválido!') 

    # Imprime a resposta recebida do servidor
    if message != '': print(message)

# Fecha a conexão do socket
clientSocket.close()
