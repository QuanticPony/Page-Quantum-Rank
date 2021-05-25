#%%
import numpy as np

from qutip.steadystate import steadystate

from funciones import *

from pyvis.network import Network


from matplotlib import pyplot as plt

import pickle

import networkx as nx
import matplotlib.pyplot as plt

if __name__=='__main__':

    Quantum = True
    Classic = True
    Google = True
    
    n_nodes=41
    A_ij = read_links('links-sin-bots.txt', n_nodes)

    # Leemos correspondencia entre nombre y nodo del archivo de texto y lo guardamos en un diccionario
    with open('correspondencia-sin-bots.txt',encoding='latin-1', errors='replace') as corr:
        names = {}
        for line in corr:
            node, name = line.split(maxsplit=1)
            node = int(node)
            name = name[0:-1] # El replace no me funcionaba, con esto sí que me quita el \n
            names.update({node: name})
    
    PI_ij = calculate_PI(A_ij)
    G_ij = calculate_G(PI_ij, 0.9)
    
    #alpha_range = np.linspace(0,1,100)
    alpha_range = [0.9]
    
    for alpha in alpha_range:
        print(f'Valor de alpha: {alpha}')
        if Quantum:
            time_in = time()*1e-6
            H = Hamiltonian(G_ij)

            L = Liouvillian(alpha, G_ij, H)

            QR = np.zeros(n_nodes)
            p = steadystate(L)
            for i in range(n_nodes):
                QR[i] = np.real(p[i,i])
            print(f"Tiempo transcurrido: {(time()*1e-6-time_in)}ms")

        if Classic:
            PR = page_rank(A_ij, evolve, equal)
            PR = np.array(PR)

        if Google:
            GR = page_rank(A_ij, evolveG, equal)
            GR = np.array(GR)

        with open(f'datos_{alpha:.02f}.dat', 'wb') as file:
            pickle.dump([PR, QR, GR, names], file)