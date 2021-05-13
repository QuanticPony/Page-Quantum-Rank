#%%
import numpy as np
from qutip import *
from qutip.steadystate import steadystate

from funciones import *

def Liouvillian(alpha, PI_ij, H):
    n_nodes = len(PI_ij)
    _Liouvillian = -1j*(1-alpha)*(spre(H)-spost(H))
    for i in range(n_nodes):
        for j in range(n_nodes):
            if PI_ij[j][i] != 0:
                _Liouvillian += alpha * PI_ij[j][i] * lindblad_dissipator(L_ij(i,j,n_nodes))
    return _Liouvillian


if __name__=='__main__':
    n_nodes=8
    A_ij = read_links('simple-net.txt', n_nodes)
    
    PI_ij = calculate_PI(A_ij)
    G_ij = calculate_G(PI_ij)
    
    H = Hamiltonian(PI_ij)
    
    L = Liouvillian(0.8, G_ij, H)
    
    P = np.zeros(n_nodes)
    p = steadystate(L)
    for i in range(n_nodes):
        P[i] = np.real(p[i,i])
    
    print_rank(P)
    
    
    
    #print('*************************')
    #page_rank(A_ij, evolve, equal)
    #
    ##print('*************************')
    ##page_rank(A_ij, evolve_T, equal, _transpuesta=True)
    #print('*************************')
    #
    #page_rank(A_ij, evolveG, equal)
    #print('*************************')
