## 🌐 Comunicação: Cliente → Servidor 🌐

Trabalho prático da disciplina de Redes de Computadores, pela Universidade Federal de Alfenas (UNIFAL).

A ideia do projeto consiste no desenvolvimento de duas aplicações usando sockets (UDP e TCP). Cada aplicação será composta por dois módulos: cliente e servidor. 

Cada uma das aplicações implementa os seguintes comandos:

- **ls**: servidor retorna a lista de arquivos existentes no seu diretório atual.
- **pwd**: servidor retorna o caminho (path) completo do diretório atual.
- **cd <caminho_diretorio>**: servidor muda para o novo caminho
passado por parâmetro.
- **scp <caminho_arquivo>**: servidor transfere o arquivo (cujo
caminho foi passado pelo cliente) para a máquina do cliente, salvo no mesmo diretório em que se encontra a aplicação cliente.

Os comandos sempre fluem do cliente para o servidor, que retorna a respectiva resposta para o comando do cliente: _Cliente → Servidor_

### Tecnologias
<img src="https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=3670A0&labelColor=070707" alt="Python">

### Execução
Para ambas as aplicações é necessário `python3` instalado.

Para executar uma das aplicações (no exemplo a UDP), caminhe até o diretório do tipo desejado e siga os seguintes passos:

1. Abra 2 terminais, um para o cliente e um para o servidor. Eles podem ser na mesma máquina ou em máquinas separadas, um terminal em cada máquina.
2. No primeiro terminal (Servidor), caminhe para o diretório `Server` e execute o comando:

    ```
    python3 UDPServer.py
    ```
3. No segundo terminal (Cliente), caminhe para o diretório `Client` e execute o comando:

    ```
    python3 UDPClient.py <NOME_DO_SERVIDOR>
    ```
    **<NOME_DO_SERVIDOR>** é o `IP` da máquina do servidor ou `localhost`, em caso de execução na mesma máquina. 

4. Com ambos os terminais funcionando, basta usar os comandos no terminal do cliente para navegar, listar arquivos e copiar arquivos do servidor, além de observar as respostas no terminal do servidor. Seguem alguns exemplos de comandos usando os arquivos de exemplo presentes no repositório: 
    ```
    $: pwd

    // Saída

    $: ls
    
    // Saída

    $: cd ../../arc
    
    // Saída

    $: ls
    
    // Saída

    $: scp OW.jpeg
    
    // Saída

    ```

Obs: Uma das aplicações funciona com base em UDP e a outra em TCP, mas ambas tem as mesmas funcionalidades e podem ser executadas da mesma forma, basta trocar os nomes de `UDPClient.py` e `UDPServer.py` para `TCPClient.py` e `TCPServer.py`, respectivamente.

### Autores

<a href="https://github.com/gabriel-francelino" target="_blank"><img src="https://img.shields.io/static/v1?label=Github&message=Gabriel Francelino&color=f8efd4&style=for-the-badge&logo=GitHub"></a>
<a href="https://github.com/gabriel-piva" target="_blank"><img src="https://img.shields.io/static/v1?label=Github&message=Gabriel Piva&color=f8efd4&style=for-the-badge&logo=GitHub"></a>

### Referências
O código base que foi utilizado e modificado para chegar nas duas aplicações finais veio do livro _Redes de Computadores – Uma abordagem Top Down - Kurose e Ross (6a edição)_.
