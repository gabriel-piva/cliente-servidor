# Importando as bibliotecas necessárias
import socket, os

# Definindo a porta do servidor
serverPort = 12000

# Criando um objeto de soquete usando o protocolo UDP
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Vinculando o soquete do servidor a um endereço IP vazio e à porta especificada
serverSocket.bind(('', serverPort))

# Imprime mensagens vermelhas
def print_error(message):
    print('\033[91m' + message + '\033[0m')
    
# Imprime mensagens verdes
def print_success(message):
    print('\033[92m' + message + '\033[0m')
    
# Imprimindo uma mensagem para indicar que o servidor está pronto para receber conexões
print_success('O servidor está pronto para receber conexões')

# Comando pwd
def pwd_command(clientAddress):
    current_dir = os.getcwd()
    serverSocket.sendto(current_dir.encode(), clientAddress)

# Comando ls
def ls_command(clientAddress):
    # Transforma a lista de arquivos em uma string
    file_list = '\n'.join(os.listdir())
    serverSocket.sendto(file_list.encode(), clientAddress)

# Comando cd
def cd_command(clientAddress, *args):
    new_dir = args[0] 

    # Verifica se o diretório existe e muda para ele se existir
    if os.path.isdir(new_dir):
        os.chdir(new_dir)
        current_dir = os.getcwd()
        serverSocket.sendto(f'Diretório atual: {current_dir}'.encode(), clientAddress)
    else:
        serverSocket.sendto('Diretório inválido'.encode(), clientAddress)

# Comando scp
def scp_command(clientAddress, *args):
    # Recebendo o nome do arquivo
    file_name = args[0]

    # Verificando se o arquivo existe
    if os.path.exists(file_name) and os.path.isfile(file_name):
        # Manda '1' se arquivo existir
        serverSocket.sendto('1'.encode(), clientAddress)
        print_success('Tem arquivo mano.')

        # Obtem o tamanho do arquivo e envia para o cliente
        file_size = int(os.path.getsize(file_name))
        serverSocket.sendto(str(file_size).encode(), clientAddress)
        print_success(f'Tamanho do arquivo a ser enviado: {file_size} bytes')
        
        # Tamanho máximo do pacote
        max_packet_size = 1400
        
        # Abrindo arquivo para leitura binária
        file = open(file_name, 'rb')
        # Enviando os dados do arquivo para o cliente
        while file_size > 0:
            # Se o tamanho do arquivo for maior que o limite do pacote
            # será enviado o a quantidade de dados max do pacote
            if(file_size > max_packet_size):
                file_data = file.read(max_packet_size)
                serverSocket.sendto(file_data, clientAddress)
                # Espera confirmação do cliente
                serverSocket.recvfrom(2048)
                file_size -= max_packet_size
            # Se não, será enviado o tamanho que falta
            else:
                file_data = file.read(file_size)
                serverSocket.sendto(file_data, clientAddress)
                # Espera confirmação do cliente
                serverSocket.recvfrom(2048)
                file_size -= file_size
        file.close()
        print_success('Tá tudo entregue parceiro')

        # Enviando uma confirmação para o cliente
        serverSocket.sendto('Arquivo copiado com sucesso!'.encode(), clientAddress)
    else:
        # Manda '0' se arquivo não existir
        serverSocket.sendto('0'.encode(), clientAddress)
        print_error('Achei esse trem não')
        
        # Enviando uma confirmação para o cliente
        serverSocket.sendto('Arquivo não encontrado!!'.encode(), clientAddress)

# Loop principal para receber e processar as mensagens dos clientes
while True:
    # Recebendo uma mensagem e o endereço do cliente que enviou a mensagem
    message, clientAddress = serverSocket.recvfrom(2048)

    # Imprimindo a mensagem recebida do cliente
    print(f'Mensagem recebida do cliente: \033[1;34m{message.decode()}\033[0m')
 
    # Separando o comando dos argumentos
    command, *args = message.decode().strip().split()
    args = args if len(args) > 0 else [' ']

    # Execução dos comando
    if command == 'pwd':     
        pwd_command(clientAddress)
    elif command == 'ls':
        ls_command(clientAddress)
    elif command == 'cd':
        cd_command(clientAddress, *args)
    elif command == 'scp':
        scp_command(clientAddress, *args)
    elif command == 'exit':
        break
    else:
        serverSocket.sendto('Comando inválido'.encode(), clientAddress)

# Fechando o soquete do servidor
serverSocket.close()