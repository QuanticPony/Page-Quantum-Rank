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
    
    n_nodes=8
    A_ij = read_links('simple-net.txt', n_nodes)

    # Leemos correspondencia entre nombre y nodo del archivo de texto y lo guardamos en un diccionario
    with open('names.txt', encoding='UTF-8', errors='replace') as corr:
        names = {}
        for line in corr:
            node, name = line.split(maxsplit=1)
            node = int(node)
            name = name[0:-1] # El replace no me funcionaba, con esto sí que me quita el \n
            names.update({node: name})
    
    PI_ij = calculate_PI(A_ij)
    G_ij = calculate_G(PI_ij, 0.9)
    
    alpha_range = np.linspace(0.1,1,20)
    alpha_range = [1]
    for style in ['mean']:#'max','min','norm','diff']:
        H = Hamiltonian(G_ij, style=style)
        
        GR = page_rank(A_ij, evolveG, equal)
        GR = np.array(GR)
        PR = page_rank(A_ij, evolve, equal)
        PR = np.array(PR)
                
        for alpha in alpha_range:
            time_in = time()*1e-6
            print(f'Valor de alpha: {alpha:.2f}')
            
            L = Liouvillian(alpha, G_ij, H)
    
            QR = np.zeros(n_nodes)
            p = steadystate(L)
            for i in range(n_nodes):
                QR[i] = np.real(p[i,i])
            print(f"Tiempo transcurrido: {(time()*1e-6-time_in)}ms")
    
            with open(f'{style}/datos_{alpha:.02f}.dat', 'wb') as file:
                pickle.dump([PR, QR, GR, names], file)
        
        
        print_rank(PR, names=names)
        print_rank(GR, names=names)
        print_rank(QR, names=names)
        
#%%  
    #plt.style.use('fast')
    #
    #p_PR = np.argsort(PR)[::-1]
    #p_QR = np.argsort(QR)[::-1]
    #p_GR = np.argsort(GR)[::-1]
    #
    #plt.scatter(p_GR, p_QR-p_GR)
    ##plt.scatter(np.arange(0,40), p_QR)
    ##plt.scatter(np.arange(0,40), p_GR)
    #plt.xlabel('Posición PR')
    #plt.ylabel('(Posición QR) - (Posición PR)')

    #with open('datos.dat', 'wb') as file:
    #    pickle.dump([PR, QR, GR, names], file)

    #print_rank(PR, names=names)



#    Pintamos la red
    # netp = Network(directed=True, height="100%", width='100%', bgcolor='#222222', font_color='white')
    # netq = Network(directed=True, height="100%", width='100%', bgcolor='#222222', font_color='white')
    # netg = Network(directed=True, height="100%", width='100%', bgcolor='#222222', font_color='white')
    
    # netp.barnes_hut()
    # netq.barnes_hut()
    # netg.barnes_hut()


    # Creo un array de la gente que no tiene links para no representarlos en el gráfico (inspección directa)
    # gente_sin_links = []#'FisBot', 'FisBot_develop', 'Groovy', 'Manuel Vivas', 'Miguel Tajada']

    # for i in range(n_nodes):
        # if names[i+1] not in gente_sin_links:
            # netp.add_node(i, label=names[i+1], size=(PR[i]/max(PR)*50))
            # netq.add_node(i, label=names[i+1], size=(QR[i]/max(QR)*50))
            # netg.add_node(i, label=names[i+1], size=(GR[i]/max(GR)*50))

    # for i in range(n_nodes):
        # for j in range(n_nodes):
            # if A_ij[i][j] != 0:
                # netp.add_edge(i,j, value=A_ij[i][j])
                # netq.add_edge(i,j, value=A_ij[i][j])
                # netg.add_edge(i,j, value=A_ij[i][j])
    # 
    # netp.show('net_p.html')
    # netq.show('net_q.html')
    # netg.show('net_g.html')
# %%

    #Pintamos la red
    # net = Network(directed=True, height="100%", width='100%', bgcolor='#222222', font_color='white')
    # net.barnes_hut()
        

    # # Creo un array de la gente que no tiene links para no representarlos en el gráfico (inspección directa)
    # gente_sin_links = ['FisBot', 'FisBot_develop', 'Groovy', 'Manuel Vivas', 'Miguel Tajada']

    # for i in range(n_nodes):
    #     if names[i+1] not in gente_sin_links:
    #         net.add_node(i, label=names[i+1], size=(10+PR[i]/max(PR)*40))
        
    # for i in range(n_nodes):
    #     for j in range(n_nodes):
    #         if A_ij[i][j] != 0:
    #             net.add_edge(i,j, value=A_ij[i][j])
    
    # net.show('ejemplo.html')

    #pruebo con otra librería

