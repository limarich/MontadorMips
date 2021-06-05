teste = []
lista = []
teste.append("aqui é codigo #aqui é comentario")
teste.append("aqui é outro codigo #aqui nao")
def retiraComentario(string):#str
    l = string.split("#")#faço split e jogo pra lista
    l.pop()#retirei o que não desejo
    return l#retorno uma lista
for t in teste:
    lista.append(retiraComentario(t))
print(lista)