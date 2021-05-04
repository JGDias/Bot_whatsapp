legenda = './legenda.txt'
legenda_2 = './legenda_2.txt'
arq = open(legenda, 'r')
arq2 = open(legenda_2, 'w')
contador = 0
lista = arq.readlines()
tamanho = len(lista)
for y in range(tamanho) :
    if lista[y-contador] == '\n':
        lista.pop(y-contador)
        contador += 1
    elif lista[y-contador] == 'i\n':
        lista.pop(y-contador)
        contador += 1
lista2 = lista

for item in lista2:
    arq2.write(item)