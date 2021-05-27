import numpy as np

from qutip.steadystate import steadystate

from funciones import *

from pyvis.network import Network


if __name__=='__main__':

    Quantum = True
    Classic = False
    Google = False

    n_nodes=40
    A_ij = read_links('links-sin-Leyre.txt', n_nodes)

    # Leemos correspondencia entre nombre y nodo del archivo de texto y lo guardamos en un diccionario
    with open('correspondencia_sin_Leyre.txt',encoding='UTF-8', errors='replace') as corr:
        names = {}
        for line in corr:
            node, name = line.split(maxsplit=1)
            node = int(node)
            name = name[0:-1] # El replace no me funcionaba, con esto sí que me quita el \n
            names.update({node: name})

    #Leemos links de fotos
    with open('fotitos_sin_Leyre.txt',) as ph:
        fotos = []
        for line in ph:
            fotos.append(line)

    PI_ij = calculate_PI(A_ij)
    G_ij = calculate_G(PI_ij)
    
    if Quantum:
        H = Hamiltonian(G_ij, style='mean')
        
        L = Liouvillian(1, G_ij, H)
        
        PR = np.zeros(n_nodes)
        p = steadystate(L)
        for i in range(n_nodes):
            PR[i] = np.real(p[i,i])

        print('Algoritmo cuántico')
    
    
    if Classic:
        PR = page_rank(A_ij, evolve, equal)
        print('Algoritmo clásico')


    if Google:
        PR = page_rank(A_ij, evolveG, equal)
        print('Algoritmo de Google')

    print_rank(PR, names=names)


    #Pintamos la red
    net = Network(directed=True, height="100%", width='100%', bgcolor='#242e41', font_color='white')
    net.barnes_hut()
    net.show_buttons()

    for i in range(n_nodes):
        net.add_node(i, label=names[i+1], size=(10+PR[i]/max(PR)*40), shape='image', image=fotos[i])

    for i in range(n_nodes):
        for j in range(n_nodes):
            if A_ij[i][j] != 0:
                net.add_edge(i,j, value=A_ij[i][j], color='cornflowerblue')
    
    net.show('ejemplo.html')