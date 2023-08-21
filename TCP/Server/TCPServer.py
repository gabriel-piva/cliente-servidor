# Importando as bibliotecas necessárias
import socket, os

# Define a porta do servidor
serverPort = 12000

# Cria um socket TCP
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket ao endereço do servidor e porta
serverSocket.bind(('', serverPort))

# O socket entra em modo de escuta, permitindo uma conexão
serverSocket.listen(1)

# Imprime mensagens vermelhas
def print_error(message):
    print('\033[91m' + message + '\033[0m')

# Imprime mensagens verdes
def print_success(message):
    print('\033[92m' + message + '\033[0m')
    
# Imprimindo uma mensagem para indicar que o servidor está pronto para receber conexões
print_success('O servidor está pronto para receber conexões')

# Aguarda uma conexão de um cliente
connectionSocket, addr = serverSocket.accept()

# * Definindo funções dos camandos

# Comando pwd
def pwd_command():
    # Obtém o diretório atual
    current_dir = os.getcwd()
    connectionSocket.send(current_dir.encode())
    connectionSocket.recv(1024)
    
# Comando ls
def ls_command():
    # Transforma a lista de arquivos em uma string
    file_list = '\n'.join(os.listdir())
    connectionSocket.send(file_list.encode())
    connectionSocket.recv(1024)
    
# Comando cd
def cd_command(*args):
    new_dir = args[0]
    if os.path.isdir(new_dir):
        os.chdir(new_dir)
        current_dir = os.getcwd()
        connectionSocket.send(f'Diretório atual: {current_dir}'.encode())
        connectionSocket.recv(1024)
    else:
        connectionSocket.send('Diretório inválido'.encode())
        connectionSocket.recv(1024)

# Comando scp
def scp_command(*args):
    file_name = args[0]
    
    # Verificando se o arquivo existe
    if os.path.exists(file_name) and os.path.isfile(file_name):
        # Manda '1' se arquivo existir
        connectionSocket.send('1'.encode())
        connectionSocket.recv(1024)
        print_success('Tem arquivo mano.')
        
        # Obtém o tamanho do arquivo e enviando para o cliente
        file_size = os.path.getsize(file_name)
        connectionSocket.send(str(file_size).encode())
        connectionSocket.recv(1024)
        print_success(f'Tamanho do arquivo a ser enviado: {file_size} bytes')
        
        # Tamanho máximo do pacote
        max_packet_size = 1400
        
        # Abrindo o arquivo para leitura binária
        file = open(file_name, 'rb')
        # Enviando os dados do arquivo para o cliente
        while file_size > 0:
            # Se o tamanho do arquivo for maior que o limite do pacote
            # será enviado a quantidade de dados max do pacote 
            if(file_size > max_packet_size):
                file_data = file.read(max_packet_size)
                connectionSocket.send(file_data)
                # Espera confirmação do cliente
                connectionSocket.recv(1024)
                file_size -= max_packet_size
            # Se não, será enviado o tamanho que falta
            else:
                file_data = file.read(file_size)
                connectionSocket.send(file_data)
                # Espera confirmação do cliente
                connectionSocket.recv(1024)
                file_size -= file_size
        file.close()
        print_success('Tá tudo entregue parceiro.')
        
        # Enviando uma confirmação para o cliente
        connectionSocket.send('Arquivo copiado com sucesso!'.encode())
        connectionSocket.recv(1024)
    else:
        # Manda '0' se arquivo não existir
        connectionSocket.send('0'.encode())
        connectionSocket.recv(1024)
        print_error('Achei esse trem não.')
        
        # Enviando uma confirmação para o cliente
        connectionSocket.send('Arquivo não encontrado!'.encode())
        connectionSocket.recv(1024)
        
while True:
    # Recebe a sentença enviada pelo cliente através da conexão
    sentence, _ = connectionSocket.recvfrom(1024)
    connectionSocket.send('ACK'.encode())
    print(f'Mensagem recebida do cliente: \033[1;34m{sentence.decode()}\033[0m')
    
    # Separando o comando dos argumentos
    command, *args = sentence.decode().strip().split()
    args = args if len(args) > 0 else [' ']
    
    if(command == 'pwd'):
        pwd_command()
    elif(command == 'ls'):
        ls_command()
    elif(command == 'cd'):
        cd_command(*args)
    elif(command == 'scp'):
        scp_command(*args)
    elif(command == 'exit'):
        break
    else:
        connectionSocket.send('Comando inválido'.encode())

# Fecha a conexão do socket após a resposta ter sido enviada
connectionSocket.close()
serverSocket.close()
