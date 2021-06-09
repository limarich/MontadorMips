# string = "00000000111111112222222233333333"
# temp = []
# temp.append(string[0:8])
# temp.append(string[8:16])
# temp.append(string[16:24])
# temp.append(string[24:32])
# print(temp)
# def bitNot(num):
#     string = ''
#     for ch in num:
#         if(ch == '1'):
#             string+='0'
#         elif(ch == '0'):
#             string+='1'
#         else:
#             print("erro")
#     return string
# def complemento2(num):
#     string = ''
#     # if(num[-1] == '0'):
#     if(num[-1] == '1'):
#         aux = 0
#         for ch in range(len(num)):
#             if(num[ch] == '1'):
#                 string += '0'
#             else:
#                 string += '1'
#                 aux = ch + 1
#                 break
#         for i in range(aux,len(num)):
#              string += num[i]
#     return string
# var = -10
# var *= -1
# string = complemento2(bitNot(format(var,"b")))
# print(string[:-1])
# print(bin(10))
var = -8
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
    temp = format(num, 'b')
    saida = complemento1(temp)
    return soma1(saida)
print(complemento2(var))
