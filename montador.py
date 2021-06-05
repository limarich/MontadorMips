import sys
nda = 0
linhas = [] #recebe as linhas do código
tokens = [] #tokens dos codigos
shamt = "00000"
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
    global comentario
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
                    tokens.append(Token(token,'J',"000010",0)) #j
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
                tokens.append(Token(string, nda,nda,format(int(string),"b")))#numeros
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
                tokens.append(Token(token,'R',"000000","100000"))#add
                token = ''
            elif(str == 'd'):
                chave = 3
                token += 'd'
        elif(chave == 3):
            if(str == 'i'):
                chave = 0
                token += 'i'
                tokens.append(Token(token,'I',"001000",nda))#addi
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
                tokens.append(Token(token,'I',"101011",nda)) #sw
                token = 0
            else:
                print('erro')
        elif(chave == 5):
            if(str == 'b'):
                chave = 0
                token += 'b'
                tokens.append(Token(token,'R',"000000","100010")) #sub
                token = ''
        elif(chave == 6):
            if(str == 't'):
                chave = 0
                token += 't'
                tokens.append(Token(token, 'R',"000000","101010"))#slt
                token = ''
        elif(chave == 7):
            if(str == 'd'):
                chave = 0
                token += 'd'
                tokens.append(Token(token, 'R',"000000","100100"))#and
                token = ''
        elif(chave == 8):
            if(str == 'r'):
                chave = 0
                token += 'r'
                #or/xor
                if(string == 'or'):
                    tokens.append(Token(token,'R',"000000","100101"))
                else:
                    tokens.append(Token(token,'R',"000000","100110"))
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
                tokens.append(Token(token,'I', "000100", nda))#beq
                token = ''
        elif(chave == 12): 
            if(str == 'e'):
                chave = 0
                token += "e"
                tokens.append(Token(token, 'I', "000101", nda))#bne
                token = ''
        elif(chave == 13):
            if(str == 'a'):
                chave = 14
                token += 'a'
            elif(str == 'r'):
                chave = 0
                token += 'r'
                tokens.append(Token(token, 'R', "000000", "001000")) #jr
                token = 0
        elif(chave == 14):
            if(str == 'l'):
                chave = 0
                token += 'l'
                tokens.append(Token(token, 'J', "000011",nda))#jal
                token = 0
        elif(chave == 15):
            if(str == 'w'):
                chave = 0
                token += 'w'
                tokens.append(Token(token, 'I', "100011", nda))#lw
                token = ""
        elif(chave == 16):
            if(string == '$zero'):
                chave = 0
                token = ""
                tokens.append(Token('$zero','registrador',nda,'00000')) #zero
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
                tokens.append(Token(token, 'registrador',nda,"00001"))#at
                token = ''
            elif(int(str) >= 0 and int(str) <= 3):
                chave = 0
                token += str
                if(int(str) == 0):
                    tokens.append(Token(token, 'registrador',nda,"00100"))#a0
                elif(int(str) == 1):
                    tokens.append(Token(token, 'registrador',nda,"00101"))#a1
                elif(int(str) == 2):
                    tokens.append(Token(token, 'registrador',nda,"00110"))#a2
                elif(int(str) == 3):
                    tokens.append(Token(token, 'registrador',nda,"00111"))#a3
        elif(chave == 18): 
            if(int(str) == 0 or int(str) == 1):
                token+=str
                chave = 0
                if(int(str) == 0):
                    tokens.append(Token(token, 'registrador',nda,"11010"))#k0
                elif(int(str) == 1):
                    tokens.append(Token(token, 'registrador',nda,"11011"))#k1
                token = ''
        elif(chave == 19):
            if(int(str) >= 0 and int(str) <= 9):
                chave = 0
                token += str
                if(int(str) == 0):
                    tokens.append(Token(token, 'registrador',nda,"01000"))#t0
                if(int(str) == 1):
                    tokens.append(Token(token, 'registrador',nda,"01001"))#t1
                if(int(str) == 2):
                    tokens.append(Token(token, 'registrador',nda,"01010"))#t2
                if(int(str) == 3):
                    tokens.append(Token(token, 'registrador',nda,"01011"))#t3
                if(int(str) == 4):
                    tokens.append(Token(token, 'registrador',nda,"01100"))#t4
                if(int(str) == 5):
                    tokens.append(Token(token, 'registrador',nda,"01101"))#t5
                if(int(str) == 6):
                    tokens.append(Token(token, 'registrador',nda,"01110"))#t6
                if(int(str) == 7):
                    tokens.append(Token(token, 'registrador',nda,"01101"))#t7
                if(int(str) == 8):
                    tokens.append(Token(token, 'registrador',nda,"11000"))#t8
                if(int(str) == 9):
                    tokens.append(Token(token, 'registrador',nda,"11001"))#t9
                token = ''
        elif(chave == 20):
            if(str == 'p'):
                chave = 0
                token += 'p'
                tokens.append(Token(token,'registrador',nda,"11101"))#sp
                token =''
            elif(int(str) >= 0 and int(str) <= 7):
                chave = 0
                token += str
                if(int(str) == 0):
                    tokens.append(Token(token, 'registrador',nda,'10000'))#s0
                elif(int(str) == 1):
                    tokens.append(Token(token, 'registrador',nda,'10001'))#s1
                elif(int(str) == 2):
                    tokens.append(Token(token, 'registrador',nda,'10010'))#s2
                elif(int(str) == 3):
                    tokens.append(Token(token, 'registrador',nda,'10011'))#s3
                elif(int(str) == 4):
                    tokens.append(Token(token, 'registrador',nda,'10100'))#s4
                elif(int(str) == 5):
                    tokens.append(Token(token, 'registrador',nda,'10101'))#s5
                elif(int(str) == 6):
                    tokens.append(Token(token, 'registrador',nda,'10110'))#s6
                elif(int(str) == 7):
                    tokens.append(Token(token, 'registrador',nda,'10011'))#s7
                token =''
        elif(chave == 21):
            if(str == 'p'):
                chave = 0
                token += 'p'
                if(string == '$fp'):
                    tokens.append(Token(token,'registrador',nda,"11110"))#fp
                if(string == '$gp'):
                    tokens.append(Token(token,'registrador',nda,"11100"))#gp
                token =''
        elif(chave == 22):
            if(str == 'a'):
                chave = 0
                token += 'a'
                tokens.append(Token(token, 'registrador',nda,"11111"))#ra
        else:
            chave = 0
            erro = f"sintaxe inválida: {token}"
            print(erro)
            token = ''
"""
 uma função que faz a leitura de cada linha e passa para a lerCodigo
 """
def lerLinhas():
    global comentario
    for l in range(len(linhas)): 
        try:
            lerCodigo(linhas[l])
            # print((l))
        except:
            print(f"sintaxe invalida -->{erro}\n")
            quit()
def eqPrecisao(binario): #ajeita a precisao deixa a mesma para todos os inteiros fornecidos
    while(len(binario) != 16):
        binario = "0" + binario 
    return binario
lerLinhas()
#lê cada token
code = []
codigo=""
while len(tokens) > 0:
    if(tokens[0].tipo == 'R'):
        codigo += tokens[0].opcode + tokens[1].funct + tokens[2].funct + tokens[3].funct + shamt + tokens[0].funct #op+rs+rt+rd+shamt+func
        for i in range(0, 4):#retira os 4 primeiros
            tokens.pop(0)
        code.append(codigo)
        codigo = ''
    # elif(tk.tipo == 'J'):
    elif(tokens[0].tipo == 'I'):
        if(tokens[0].token == 'addi'):
            codigo += tokens[0].opcode + tokens[1].funct + tokens[2].funct + eqPrecisao(tokens[3].funct)#op+rs+rt+imm
            for i in range(0, 4):#retira os 4 primeiros
                tokens.pop(0)
            code.append(codigo)
            codigo = ''
print(code)
#lidar com labels
#lidar com comentarios
#pode parenteses em caso de pilha https://d2vlcm61l7u1fs.cloudfront.net/media%2F138%2F1380baa4-79a2-4bcf-9e82-9e5e57830f26%2FphpePJ8xi.png
#lidar com erros de sintaxe
#acompanhar o endereço de cada linha(começar em 0) 