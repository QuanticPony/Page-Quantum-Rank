#%%
import numpy as np
from qutip import *
from qutip.steadystate import steadystate

from funciones import *

from pyvis.network import Network

def Liouvillian(alpha, PI_ij, H):
    n_nodes = len(PI_ij)
    _Liouvillian = -1j*(1-alpha)*(spre(H)-spost(H))
    for i in range(n_nodes):
        for j in range(n_nodes):
            if PI_ij[j][i] != 0:
                _Liouvillian += alpha * PI_ij[j][i] * lindblad_dissipator(L_ij(i,j,n_nodes))
    return _Liouvillian


if __name__=='__main__':
    n_nodes=39
    A_ij = read_links('links.txt', n_nodes)
    
    PI_ij = calculate_PI(A_ij)
    G_ij = calculate_G(PI_ij)
    
    H = Hamiltonian(PI_ij)
    
    #L = Liouvillian(0.8, G_ij, H)
    
    #P = np.zeros(n_nodes)
    #p = steadystate(L)
    #for i in range(n_nodes):
    #    P[i] = np.real(p[i,i])
    #
    #print_rank(P)
    
    
    
    #print('*************************')
    #page_rank(A_ij, evolve, equal)
    #
    ##print('*************************')
    ##page_rank(A_ij, evolve_T, equal, _transpuesta=True)
    #print('*************************')
    #
    PR = page_rank(A_ij, evolveG, equal)
    #print('*************************')
    
    net = Network(directed=True, height="2000px", width="2000px", bgcolor='#222222', font_color='white')
    net.barnes_hut()
    
    with open('correspondencia.txt') as corr:
        names = {}
        for line in corr:
            node, name = line.split(maxsplit=1)
            node = int(node)
            name.replace('\n','')
            names.update({node: name})
        
        
        for i in range(n_nodes):
            net.add_node(i, label=names[i+1], size=PR[i]/max(PR)*40)
            
        for i in range(n_nodes):
            for j in range(n_nodes):
                if A_ij[i][j] != 0:
                    net.add_edge(i,j, value=A_ij[i][j])
    
        net.show('ejemplo.html')
