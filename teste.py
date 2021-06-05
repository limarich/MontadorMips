def retiraComentario(string):
    str = ""
    for ch in string:
        if(ch != "#"):
            str += ch
        if(ch == "#"):
            break
    return str
            
arquivo = open("teste.asm", "r")
for linha in arquivo:
    print(retiraComentario(linha))
arquivo.close()