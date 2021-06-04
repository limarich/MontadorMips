import sys
registradores = [
    '$zero', '$at', '$v0', '$v1', '$a0', '$a2', '$a3', '$t0',
    '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7','$s0',
    '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7', '$t8', '$t9',
    '$k0', '$k1', '$gp', '$sp', '$fp', '$ra'
]
comandos = [
    'add', 'addi', 'sub', 'and', 'or', 'xor', 'slt', 'beq', 'bne',
    'j', 'jal', 'jr', 'lw', 'sw'
]
linhas = [] #recebe as linhas do código
tokens = [] #tokens dos codigos
erro = ""
"""
carrega o arquivo passado no console
"""
def loadFile(fileName):
    global linhas
    aux = [] #lista auxiliar recebe todos os itens da linha
    arquivo  = open(fileName, "r")
    for linha in arquivo: #para cada linha do arquivo
        temp = linha.split(",") #separa as virgulas
        for l in temp:
            aux.append(l.split()) #separa os espaços e coloca na lista auxiliar
    for item in aux:
        for i in item:
            linhas.append(i) #junta todos os itens numa lista só
    # print(linhas)
    arquivo.close()

# nomeArquivo  = sys.argv[1] #para ler pelo console

loadFile("teste.asm") #nomeArquivo
# print(linhas)
"""
#para rodar use: python montador.py nomeDoArquivo.asm
"""
"""
Classe de erro de sintaxe
"""
class InvalidSyntax(Exception):
    def __init__(self):
        pass
    """
Classe de tokens
    """
class Token():
    def __init__(self, token, t):
        self.token = token
        self.t = t
def lerCodigo(string):
    """
        realiza a leitura do arquivo carregado e verifica a escrita mediante a uma chave de controle
    """
    global tokens
    global erro
    token = ''
    chave = 0 
    for str in string: 
        if(chave == 0): #add/addi
            if(str == 'a'):
                chave = 1
                token +='a'
            elif(str == 's'):#sub/slt/sw
                chave = 4
                token += 's'
            elif(str == 'o'):
                chave = 8
                token += 'o'
            elif(str=='x'):
                chave = 9
                token += 'x'
            elif(str=='b'):
                chave = 10
                token += 'b'
            elif(str=='j'):
                if((string) == (str)):
                    chave = 0
                    token += 'j'
                    tokens.append(Token(token,'comando'))
                    token = 0
                else:    
                    chave = 13
                    token += 'j'
            elif(str=='l'):
                chave = 15
                token += 'l'
        elif(chave == 1):
            if(str == 'd'):
                chave = 2
                token += 'd'
            elif(str == 'n'):
                chave = 7
                token += 'n'
            else:
                chave = 0
                erro = f"{string}"
                token = ""
                raise InvalidSyntax()
        elif(chave == 2):
            if(string[-1] == 'd'):
                chave = 0
                token += 'd'
                tokens.append(Token(token,'comando'))
                token = ''
            elif(str == 'd'):
                chave = 3
                token += 'd'
        elif(chave == 3):
            if(str == 'i'):
                chave = 0
                token += 'i'
                tokens.append(Token(token,'comando'))
                token = 0
            else:
                chave = 0
                token = ''
                erro = f"sintaxe inválida: {string}"
                raise InvalidSyntax()
        elif(chave == 4):
            if(str == 'u'):
                chave = 5
                token += 'u'
            elif(str == 'l'):
                chave = 6
                token += 'l'
            elif(str == 'w'):
                chave = 0
                token += 'w'
                tokens.append(Token(token,'comando'))
                token = 0
            else:
                print('erro')
        elif(chave == 5):
            if(str == 'b'):
                chave = 0
                token += 'b'
                tokens.append(Token(token,'comando'))
                token = ''
        elif(chave == 6):
            if(str == 't'):
                chave = 0
                token += 't'
                tokens.append(Token(token, 'comando'))
                token = ''
        elif(chave == 7):
            if(str == 'd'):
                chave = 0
                token += 'd'
                tokens.append(Token(token, 'comando'))
                token = ''
        elif(chave == 8):
            if(str == 'r'):
                chave = 0
                token += 'r'
                tokens.append(Token(token,'comando'))
                token = ''
        elif(chave == 9):
            if(str == 'o'):
                chave = 8
                token += 'o'
        elif(chave == 10):
            if(str == 'e'):
                chave = 11
                token += 'e'
            elif(str == 'n'):
                chave = 12
                token += 'n'
        elif(chave == 11):
            if(str == 'q'):
                chave = 0
                token += 'q'
                tokens.append(Token(token,'comando'))
                token = ''
        elif(chave == 12): 
            if(str == 'e'):
                chave = 0
                token += "e"
                tokens.append(Token(token, 'comando'))
                token = ''
        elif(chave == 13):
            if(str == 'a'):
                chave = 14
                token += 'a'
            elif(str == 'r'):
                chave = 0
                token += 'r'
                tokens.append(Token(token, 'comando'))
                token = 0
        elif(chave == 14):
            if(str == 'l'):
                chave = 0
                token += 'l'
                tokens.append(Token(token, 'comando'))
                token = 0
        elif(chave == 15):
            if(str == 'w'):
                chave = 0
                token += 'w'
                tokens.append(Token(token, 'comando'))
                token = ""
        else:
            chave = 0
            erro = f"sintaxe inválida: {token}"
            print(erro)
            token = ''
"""
 uma função que faz a leitura de cada linha e passa para a lerCodigo
 """
def lerLinhas():
    for l in linhas:
        # for m in l: 
        try:
            lerCodigo(l)
            # print((l))
        except:
            print(f"sintaxe invalida -->{erro}\n")
            quit()
lerLinhas()
for tk in tokens:
    print(tk.token+'\n')
#lidar com labels
#lidar com comentarios
#lidar com registradores
#lidar com endereco de memoria caso use
#lidar com conversao para binario
#converter o codigo em binario
#lidar com erros de sintaxe