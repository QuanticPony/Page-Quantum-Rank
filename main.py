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
    
    if Quantum:
        time_in = time()*1e-6
        H = Hamiltonian(G_ij)
        
        L = Liouvillian(0.9, G_ij, H)
        
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

    with open('datos.dat', 'wb') as file:
        pickle.dump([PR, QR, GR, names], file)

    #print_rank(PR, names=names)



#    Pintamos la red
    # netp = Network(directed=True, height="100%", width='100%', bgcolor='#222222', font_color='white')
    # netq = Network(directed=True, height="100%", width='100%', bgcolor='#222222', font_color='white')
    # netg = Network(directed=True, height="100%", width='100%', bgcolor='#222222', font_color='white')
    # 
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

   #FisCord = nx.DiGraph()

   #lista_Red = []

   #for j,column in enumerate(A_ij):
   #    for elto in column.keys():
   #        lista_Red.append((names[elto+1], names[j+1], A_ij[j][elto]))

   #FisCord.add_weighted_edges_from(lista_Red)

   #

   ## plt.subplot(121)
   ## nx.draw(FisCord, with_labels=True, font_weight='bold')
   ## plt.subplot(122)
   ## nx.draw_shell(FisCord, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')

   ## plt.show()

   #FC_clustering=nx.clustering(FisCord)
   #cluster=sum(FC_clustering.values())/len(FC_clustering.values())
   #print(f"clustering: {cluster:.4}")

   #pearson=nx.degree_pearson_correlation_coefficient(FisCord)
   #print(f"asortatividad (r): {pearson:.4}")
