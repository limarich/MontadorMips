import sys
nda = 0 
linhas = [] #recebe as linhas do código
tokens = [] #tokens dos codigos
offset = []
labels = {}
code = []
shamt = "00000"
erro = ""
"""
carrega o arquivo passado no console
"""
entrada  = sys.argv[1] #para ler pelo console
saida = ""
if len(sys.argv) <= 2:
    saida = "memoria.dat"
else:
    saida = sys.argv[2]
def isValid():#verifica se o nome do arquivo esta dentro do esperado
    if entrada.find('.asm') == -1:
        print("=-"*20+"\nformato de entrada não suportado!!!\n"+"=-"*20)
        quit()
    if saida.find('.dat') == -1:
        print("=-"*20,"\nformato de saida não suportado!!!\n"+"=-"*20)
        quit()
def retiraParenteses(lista):
    temp = []
    temp2 = []
    for l in lista:
        temp.append(l.split("("))
    for t2 in temp:
        for t3 in t2:
            temp2.append(t3.split(")"))
    return temp2
def retiraComentario(string):
    str = ""
    for ch in string:
        if(ch != "#"):
            str += ch
        if(ch == "#"):
            break
    return str
def loadFile(fileName):
    isValid()
    global linhas
    temp1 = []
    linha2 = []
    aux = [] #lista auxiliar recebe todos os itens da linha
    arquivo  = open(fileName, "r")
    for linha in arquivo: #retira comentario de cada linha
        temp1.append(retiraComentario(linha))
    linha2 = retiraParenteses(temp1)
    for linha3 in linha2:
        for linha in linha3:    
            temp = linha.split(",") #separa as virgulas
            for l in temp:
                aux.append(l.split()) #separa os espaços e coloca na lista auxiliar
    for item in aux:
        for i in item:
            linhas.append(i) #junta todos os itens numa lista só
    arquivo.close() 
def complemento1(binario):
    saida = ''
    for i in range(len(binario)):
        if(binario[i] == '0'):
            saida += '1'
        elif(binario[i] == '1'):
            saida += '0'
    return saida
def soma1(binario):
    saida = ''
    # print(binario)
    if(binario[-1] == '0'):
        saida = binario[:-1]
        saida += '1'
    else:
        cont = len(binario) - 2
        if(binario[cont] == '0'):
            saida = binario[:-2]
            saida+= '1'
        else:
            saida = soma1(binario[:-1])
        saida += '0'
    return saida
def complemento2(num):
    temp = ''
    num *= -1
    temp = eqPrecisao(format(num, 'b'),16)
    saida = complemento1(temp)
    return soma1(saida)

loadFile(entrada) #nomeArquivo
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
        if(labels.get(string) != None):
            tokens.append(Token(labels.get(string),"offset",nda,nda))
            break
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
                    token = ""
                else:    
                    chave = 13
                    token += 'j'
            elif(str=='l'):
                chave = 15
                token += 'l'
            elif(str == '$'):
                chave = 16
                token+='$'
            elif(string.isdigit() or str == '-' or string[:2] == '0x'):
                chave = 0
                if(str == '-'):                  
                    tokens.append(Token(string, nda,nda,complemento2(int(string))))
                elif(string[:2] == '0x'):
                    tokens.append(Token(string, nda, nda, eqPrecisao((format(int(string,16),"b")),16)))
                else:
                    tokens.append(Token(string, nda,nda,format(int(string),"b")))#numeros
                break
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 1):
            if(str == 'd'):
                chave = 2
                token += 'd'
            elif(str == 'n'):
                chave = 7
                token += 'n'
            else:
                chave = 0
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
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 3):
            if(str == 'i'):
                chave = 0
                token += 'i'
                tokens.append(Token(token,'I',"001000",nda))#addi
                token = 0
            else:
                chave = 0
                token = ''
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
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 5):
            if(str == 'b'):
                chave = 0
                token += 'b'
                tokens.append(Token(token,'R',"000000","100010")) #sub
                token = ''
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 6):
            if(str == 't'):
                chave = 0
                token += 't'
                tokens.append(Token(token, 'R',"000000","101010"))#slt
                token = ''
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 7):
            if(str == 'd'):
                chave = 0
                token += 'd'
                tokens.append(Token(token, 'R',"000000","100100"))#and
                token = ''
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 8):
            if(str == 'r'):
                chave = 0
                token += 'r'
                #or/xor
                if(string == 'or'):
                    tokens.append(Token(token,'R',"000000","100101"))#or
                else:
                    tokens.append(Token(token,'R',"000000","100110"))#xor
                token = ''
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 9):
            if(str == 'o'):
                chave = 8
                token += 'o'
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 10):
            if(str == 'e'):
                chave = 11
                token += 'e'
            elif(str == 'n'):
                chave = 12
                token += 'n'
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 11):
            if(str == 'q'):
                chave = 0
                token += 'q'
                tokens.append(Token(token,'I', "000100", nda))#beq
                token = ''
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 12): 
            if(str == 'e'):
                chave = 0
                token += "e"
                tokens.append(Token(token, 'I', "000101", nda))#bne
                token = ''
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 13):
            if(str == 'a'):
                chave = 14
                token += 'a'
            elif(str == 'r'):
                chave = 0
                token += 'r'
                tokens.append(Token(token, 'R', "000000", "001000")) #jr
                token = 0
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 14):
            if(str == 'l'):
                chave = 0
                token += 'l'
                tokens.append(Token(token, 'J', "000011",nda))#jal
                token = 0
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 15):
            if(str == 'w'):
                chave = 0
                token += 'w'
                tokens.append(Token(token, 'I', "100011", nda))#lw
                token = ""
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 16):
            if(string == '$zero'):
                chave = 0
                token = ""
                tokens.append(Token('$zero','registrador',nda,'00000')) #zero
                break
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
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
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
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 18): 
            if(int(str) == 0 or int(str) == 1):
                token+=str
                chave = 0
                if(int(str) == 0):
                    tokens.append(Token(token, 'registrador',nda,"11010"))#k0
                elif(int(str) == 1):
                    tokens.append(Token(token, 'registrador',nda,"11011"))#k1
                token = ''
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
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
                    tokens.append(Token(token, 'registrador',nda,"01111"))#t7
                if(int(str) == 8):
                    tokens.append(Token(token, 'registrador',nda,"11000"))#t8
                if(int(str) == 9):
                    tokens.append(Token(token, 'registrador',nda,"11001"))#t9
                token = ''
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
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
                    tokens.append(Token(token, 'registrador',nda,'10111'))#s7
                token =''
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 21):
            if(str == 'p'):
                chave = 0
                token += 'p'
                if(string == '$fp'):
                    tokens.append(Token(token,'registrador',nda,"11110"))#fp
                if(string == '$gp'):
                    tokens.append(Token(token,'registrador',nda,"11100"))#gp
                token =''
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        elif(chave == 22):
            if(str == 'a'):
                chave = 0
                token += 'a'
                tokens.append(Token(token, 'registrador',nda,"11111"))#ra
            else:
                chave = 0
                token = ''
                raise InvalidSyntax()
        else:
            chave = 0
            token = ''
            raise InvalidSyntax()
"""
 uma função que faz a leitura de cada linha e passa para a lerCodigo
 """
def lerLinhas():
    for l in range(len(linhas)): 
        try:
            lerCodigo(linhas[l])
        except:
            print("=-"*20 +"\n"+ f"sintaxe invalida -->{linhas[l]}\n" + "=-"*20)
            quit()
def eqPrecisao(binario,qtd): #ajeita a precisao deixa a mesma para todos os inteiros fornecidos
    while(len(binario) != qtd):
        binario = "0" + binario 
    return binario
def setOffset():
    global offset
    Pc = 0
    for tk in tokens:
        if(tk.tipo != "registrador" and tk.tipo != 0):
                offset.append(eqPrecisao(format(Pc, "b"),16))
                Pc+=4
def tradutor():
    codigo=""
    global tokens
    while len(tokens) > 0:
        if(tokens[0].tipo == 'R' and tokens[0].token == "jr"):
            codigo += tokens[0].opcode + tokens[1].funct + eqPrecisao(shamt,15) + tokens[0].funct #op+rs+shamt+func
            for i in range(0, 2):#retira os 4 primeiros
                tokens.pop(0)
            code.append(codigo)
            codigo = ''
        elif(tokens[0].tipo == 'R'):
            codigo += tokens[0].opcode + tokens[2].funct + tokens[3].funct + tokens[1].funct + shamt + tokens[0].funct #op+rs+rt+rd+shamt+func
            # print(f"a token 3:{tokens[1].token}--{tokens[2].funct}")
            for i in range(0, 4):#retira os 4 primeiros
                tokens.pop(0)
            code.append(codigo)
            codigo = ''
        elif(tokens[0].tipo == 'J'):
            if(tokens[0].token == "j"):
                if(tokens[1].token[0:2] == '0x'):
                    codigo += tokens[0].opcode + eqPrecisao(tokens[1].funct,26) #op+target
                else:
                    codigo += tokens[0].opcode + eqPrecisao(tokens[1].token,26) #op+target
                for i in range(0, 2):#retira os 4 primeiros
                    tokens.pop(0)
                code.append(codigo)
                codigo = ""
            elif(tokens[0].token == "jal"):
                   codigo += tokens[0].opcode + eqPrecisao(format(int(tokens[1].token,2)+4,"b"),26) #op+target
                   for i in range(0, 2):#retira os 4 primeiros
                        tokens.pop(0)
                   code.append(codigo)
                   codigo = ""
        elif(tokens[0].tipo == 'I'):
            if(tokens[0].token == 'addi'):
                codigo += tokens[0].opcode  + tokens[2].funct + tokens[1].funct+ eqPrecisao(tokens[3].funct,16)#op+rs+rt+imm
                for i in range(0, 4):#retira os 4 primeiros
                    tokens.pop(0)
                code.append(codigo)
                codigo = ''
            elif(tokens[0].token == 'beq' or tokens[0].token == 'bne'):
                codigo += tokens[0].opcode + tokens[1].funct + tokens[2].funct + tokens[3].token #op+rs+rt+offset
                for i in range(0, 4):#retira os 4 primeiros
                    tokens.pop(0)
                code.append(codigo)
                codigo = ""
            elif(tokens[0].token == 'lw' or tokens[0].token == 'sw'):
                codigo += tokens[0].opcode + tokens[3].funct + tokens[1].funct + eqPrecisao(tokens[2].funct,16) #op+rs+offset+rt
                for i in range(0, 4):#retira os 4 primeiros
                    tokens.pop(0)
                code.append(codigo)
                codigo =""
def setLabels():
    global labels
    l = 0
    while l < len(linhas):
        if(linhas[l][-1] == ':'):
            labels[linhas[l][:-1]] = eqPrecisao(format(l,"b"),16) 
            linhas.pop(l)
        l += 1
def writeFile():
    arquivo = open(saida,'w')
    for string in code:#pega cada codigo da lista
        temp = []
        temp.append(string[0:8])
        temp.append(string[8:16])
        temp.append(string[16:24])
        temp.append(string[24:32])
        for i in range(len(temp)-1,-1,-1):
            arquivo.write(temp[i])
            arquivo.write("\n")
    arquivo.close()
#ler os labels
setLabels()
lerLinhas()
#lê cada token
setOffset()

tradutor()
writeFile()
