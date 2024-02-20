import socket
import random

#Cria a conexao TCP
def connect(port):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('127.0.0.1',port))
        print('conexao TCP estabelecida')
        return s
    except:
        print('falhou em fazer o a conexao TCP como cliente')
        return 0


#Da o estado e a recompensa que o agente recebeu
def get_state_reward(s , act):
    s.send(str(act).encode())
    data = "" 
    data_recv = False;
    while(not data_recv):
        data = s.recv(1024).decode()
        try:
            data = eval(data)
            data_recv = True
        except:
            data_recv = False

    #convert the data to decimal int
    estado = data['estado']
    recompensa = data['recompensa']

    return estado, recompensa

#inicializa a tabela
tabela = []
for i in range(96):
    tabela.append([0,0,0])

#le a tabela do arquivo
with open('resultado.txt', 'r') as arquivo:
    linhas = arquivo.readlines()
    for i in range(96):
        linha = linhas[i].split(" ")
        for j in range(3):
            tabela[i][j] = float(linha[j])

def q_learning():
    estado = 0
    recompensa = 0
    gamma = 1
    epsilon = 0
    acoes = ['left', 'right', 'jump']
    #loop de treinamento
    for i in range(1000):
        alpha = 0.25
        #escolhe a acao
        if(random.random() < epsilon):
            acao = acoes[random.randint(0,2)]
        else:
            acao = acoes[tabela[estado].index(max(tabela[estado][0], tabela[estado][1], tabela[estado][2]))]

        #recebe o novo estado e a recompensa e calcula o index do estado na tabela
        novo_estado, recompensa = get_state_reward(connect(2037), acao)
        if recompensa == -100:
            alpha = 0.05
        platforma = int(str(novo_estado)[2:7], 2)
        direcao = int(str(novo_estado)[7:9], 2)
        novo_estado = platforma*4 + direcao

        #calcula o index da acao na tabela
        acao = acoes.index(acao)

        #atualiza a tabela
        tabela[estado][acao] = tabela[estado][acao] + alpha*(recompensa + gamma*max(tabela[novo_estado][0], tabela[novo_estado][1], tabela[novo_estado][2]) - tabela[estado][acao])

        #atualiza o estado
        estado = novo_estado

q_learning()

#escreve a tabela no arquivo
with open('resultado.txt', 'w') as f:
    for i in range(96):
        for j in range(3):
            f.write((str(tabela[i][j]) + " "))
        f.write("\n")