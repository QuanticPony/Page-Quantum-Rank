with open('links.txt','r') as file_in:
    origen, destino, peso = zip(*(map(int, line.split()) for line in file_in))

origen, destino, peso = list(origen), list(destino), list(peso)

origen2, destino2, peso2 = [], [], []

for i in range(len(origen)):

    #FisBot
    if origen[i] == 4 or destino[i] == 4:
        continue
    #FisBot_develop
    if origen[i] == 25 or destino[i] == 25:
        continue
    #Groovy
    if origen[i] == 34 or destino[i] == 34:
        continue    
    
    origen2.append(origen[i])
    destino2.append(destino[i])
    peso2.append(peso[i])

open('links-sin-bots.txt', 'w').writelines(list('\t'.join(map(str, med_set)) + '\n' for med_set in zip(origen2, destino2, peso2)))