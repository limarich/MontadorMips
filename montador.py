import sys
nda = '--'
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
    def __init__(self, token, tipo, opcode, funct):
        self.token = token
        self.tipo = tipo
        self.opcode = opcode
        self.funct = funct
def lerCodigo(string):
    """
        realiza a leitura do arquivo carregado e verifica a escrita mediante a uma chave de controle
    """
    global tokens
    global erro
    token = ''
    chave = 0 
    for str in string: 
        if(chave == 0): 
            if(str == 'a'):
                chave = 1
                token +='a'
            elif(str == 's'):
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
                    tokens.append(Token(token,'J',2,0)) #j
                    token = 0
                else:    
                    chave = 13
                    token += 'j'
            elif(str=='l'):
                chave = 15
                token += 'l'
            elif(str == '$'):
                chave = 16
                token+='$'
            elif(string.isdigit()):
                chave = 0
                tokens.append(Token(string, nda,nda,nda))#numeros
                break
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
                tokens.append(Token(token,'R',0,32))#add
                token = ''
            elif(str == 'd'):
                chave = 3
                token += 'd'
        elif(chave == 3):
            if(str == 'i'):
                chave = 0
                token += 'i'
                tokens.append(Token(token,'I',8,nda))#addi
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
                tokens.append(Token(token,'I',43,nda)) #sw
                token = 0
            else:
                print('erro')
        elif(chave == 5):
            if(str == 'b'):
                chave = 0
                token += 'b'
                tokens.append(Token(token,'R',0,34)) #sub
                token = ''
        elif(chave == 6):
            if(str == 't'):
                chave = 0
                token += 't'
                tokens.append(Token(token, 'R',0,42))#slt
                token = ''
        elif(chave == 7):
            if(str == 'd'):
                chave = 0
                token += 'd'
                tokens.append(Token(token, 'R',0,36))#and
                token = ''
        elif(chave == 8):
            if(str == 'r'):
                chave = 0
                token += 'r'
                #or/xor
                if(string == 'or'):
                    tokens.append(Token(token,'R',0,21))
                else:
                    tokens.append(Token(token,'R',0,38))
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
                tokens.append(Token(token,'I', 4, nda))#beq
                token = ''
        elif(chave == 12): 
            if(str == 'e'):
                chave = 0
                token += "e"
                tokens.append(Token(token, 'I', 5, nda))#bne
                token = ''
        elif(chave == 13):
            if(str == 'a'):
                chave = 14
                token += 'a'
            elif(str == 'r'):
                chave = 0
                token += 'r'
                tokens.append(Token(token, 'R', 0, 8)) #jr
                token = 0
        elif(chave == 14):
            if(str == 'l'):
                chave = 0
                token += 'l'
                tokens.append(Token(token, 'J', 3,nda))#jal
                token = 0
        elif(chave == 15):
            if(str == 'w'):
                chave = 0
                token += 'w'
                tokens.append(Token(token, 'I', 35, nda))#lw
                token = ""
        elif(chave == 16):
            if(string == '$zero'):
                chave = 0
                token = ""
                tokens.append(Token('$zero','registrador',nda,nda))
            elif(str == 'a'):
                chave = 17
                token+='a'
            elif(str == 'v'):
                chave = 18
                token += 'v'
            elif(str == 't'):
                chave = 19
                token += 't'
            elif(str== 's'):
                chave = 20
                token+='s' 
            elif(str=='k'):
                chave = 18
                token += 'k'
            elif(str=='g'):
                chave = 21
                token+='g'
            elif(str=='f'):
                chave = 21
                token+='f'
            elif(str == 'r'):
                chave = 22
                token += 'r'
        elif(chave == 17):
            if(str == 't'):
                chave = 0
                token += 't'
                tokens.append(Token(token, 'registrador',nda,nda))
                token = ''
            elif(int(str) >= 0 and int(str) <= 3):
                chave = 0
                token += str
                tokens.append(Token(token, 'registrador',nda,nda))
        elif(chave == 18): 
            if(int(str) == 0 or int(str) == 1):
                token+=str
                chave = 0
                tokens.append(Token(token, 'registrador',nda,nda))
                token = ''
        elif(chave == 19):
            if(int(str) >= 0 and int(str) <= 9):
                chave = 0
                token += str
                tokens.append(Token(token, 'registrador',nda,nda))
                token = ''
        elif(chave == 20):
            if(str == 'p'):
                chave = 0
                token += 'p'
                tokens.append(Token(token,'registrador',nda,nda))
                token =''
            elif(int(str) >= 0 and int(str) <= 7):
                chave = 0
                token += str
                tokens.append(Token(token, 'registrador',nda,nda))
                token =''
        elif(chave == 21):
            if(str == 'p'):
                chave = 0
                token += 'p'
                tokens.append(Token(token,'registrador',nda,nda))
                token =''
        elif(chave == 22):
            if(str == 'a'):
                chave = 0
                token += 'a'
                tokens.append(Token(token, 'registrador',nda,nda))
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
    print(tk.opcode,'\n')
#lidar com labels
#lidar com comentarios
#lidar com endereco de memoria caso use
#lidar com conversao para binario
#converter o codigo em binario
#lidar com erros de sintaxe