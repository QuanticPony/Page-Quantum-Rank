from collections import defaultdict
from inspect import Attribute
from time import time_ns as time

import numpy as np
from qutip import *

cero = lambda : 0

def convert_to_list(b_ij: np.ndarray):
    '''
    Given a matrix `b_ij` it returns a list type array
    '''
    n_nodes = b_ij.shape[0]
    B_ij = [defaultdict(cero) for _ in range(n_nodes)]
    for i in range(n_nodes):
        for j in range(n_nodes):
            B_ij[i].update({j : b_ij[i][j]})
    return B_ij

def convert_to_matrix(B_ij):
    '''
    Given a matrix list type array  `B_ij` it returns a matrix
    '''
    n_nodes = len(B_ij)
    b_ij = np.zeros([n_nodes, n_nodes], dtype=np.float16)
    for i in range(n_nodes):
        for j in range(n_nodes):
            b_ij[i][j] = B_ij[i][j]
    return b_ij

def print_matrix(b_ij):
    for j in range(len(b_ij)):
        print(' '.join([f"{b_ij[i][j]:.2f}" for i in range(len(b_ij))]))

def read_links(filename, n_nodes):
    '''
    Reads a file and returns the adjacency matrix
    '''
    
    A_ij = [defaultdict(cero) for _ in range(n_nodes)]
    A_ji = [defaultdict(cero) for _ in range(n_nodes)]

    with open(filename, 'r') as file:
        try:
            for line in file:
                i,j,p = map(float,line.split())
                i, j = int(i), int(j)
                A_ij[i].update({j:A_ij[i][j]+p})
        except:
            file.seek(0,0)
            for line in file:
                i,j = map(int, line.split())
                A_ij[i].update({j:1})
    return A_ij

def transpuesta(b_ij):
    
    lenth = len(b_ij)
    b_ji = [defaultdict(cero) for _ in range(lenth)]
    for i, b_i in enumerate(b_ij):
        for j in b_i.keys():
            b_ji[j].update({i: b_i[j]})
    return b_ji

def calculate_PI(a_ij):
    '''
    Given the adjacency matrix returns the transition matrix
    '''
    n_nodes = len(a_ij)
    
    PI_ij = [defaultdict(cero) for _ in range(n_nodes)]
    
    for i, ai in enumerate(a_ij):
        PI_ij[i].update(ai.copy())
        
        out_grade = sum(ai.values())
        for j in PI_ij[i].keys():
            PI_ij[i][j] /= out_grade    
    return PI_ij


def calculate_G(PI_ij, q=0.9):
    '''
    Given the transition matrix returns the Google matrix
    '''
    n_nodes = len(PI_ij)
    F = (1-q)/(len(PI_ij)-1)
    fero = lambda : F
    
    G_ij = [defaultdict(fero) for _ in range(n_nodes)]
    
    for i, ai in enumerate(PI_ij):
        G_ij[i].update(ai.copy())
        
        out_grade = sum(ai.values())
        for j in G_ij[i].keys():
            G_ij[i][j] = (q * PI_ij[i][j]+ (i!=j)*F)   
    return G_ij

def evolve(P, PI_ij,  **kargs):
    '''
    Evolves the system a temporal discrete step using the transition matrix
    '''
    Pnew=np.zeros(len(P))
    for i in range(len(P)):
        for j in range(len(P)):
            Pnew[i] += P[j] * PI_ij[j][i]
    return Pnew     


def evolve_T(P, PI_ji,  **kargs):
    '''
    Evolves the system a temporal discrete step using the transition matrix
    '''
    Pnew=np.zeros(len(P))
    for i, PI_i in enumerate(PI_ji):
        for j, p in PI_i.items():
            Pnew[i] += P[j] * p
    return Pnew     

def evolveG(P, pi_ij, q=0.9):
    '''
    Evolves the system a temporal discrete step using the Google matrix
    '''
    G_ij = calculate_G(pi_ij, q=q)
    Pnew=np.zeros(len(P))
    for i in range(len(P)):
        for j in range(len(P)):
            Pnew[i] += P[j] * G_ij[j][i]
    return Pnew

def equal(P1,P2, delta):
    '''
    Returns `True` if all the components in `P1` and `P2` are closer than `delta`. Else returns `False`
    '''
    for i,j in zip(P1,P2):
        if abs(i-j)>delta:
            return False      
    return True


def print_rank(P, names=None):
    '''
    Prints out via terminal the nodes and the page rank given `P`
    '''
    P=P/sum(P)
    print('Pagerank:')
    t = np.argsort(P)[::-1]
    if names is not None:
        for j,i in enumerate(t):
            print(f'{j+1})', names[i+1], f"{P[i]:.6}")
    else:
        for j,i in enumerate(t):
            print(f'{j+1})', i+1, f"{P[i]:.6}")

        
        
def page_rank(a_ij, evolve_func, equal_func, *, q=0.9, P=None, max_iters=1000, delta=0.000001, _transpuesta=False):
    pi_ij = calculate_PI(a_ij)
    if _transpuesta:
        pi_ij = transpuesta(pi_ij)
        
    if P is None:
        P = np.zeros(len(a_ij))+1/len(a_ij)
    
    time_in = float(time())
    for _ in range(max_iters):
        Pnew = evolve_func(P, pi_ij, q=q)
        if equal_func(P, Pnew, delta):
            break
        P = evolve_func(Pnew, pi_ij)
    print(f'Tiempo transcurrido: {(time()-time_in)*1e-6:.6f}ms')
    return P



#operadores cuanticos

def L_ij(i,j,N=8):
    
    return basis(N,i)*(basis(N,j).dag())
    


def Hamiltonian(M_ij, style='mean'):
    N = len(M_ij)
    H=np.zeros((N,N))
    
    style_types = {
        'mean': lambda x,y: (x+y)/2,
        'max': lambda x,y: max(x,y),
        'min': lambda x,y: min(x,y),
        'norm': lambda x,y: np.sqrt(x*x + y*y),
        'diff': lambda x,y: abs(x-y)
    }
    
    for i in range(N):
        for j in range(i,N):
            if M_ij[i][j]>0 or M_ij[j][i]>0:
                H[i,j] = H[j,i]= style_types[style](M_ij[i][j], M_ij[j][i])
        
    #for i in range(N):
    #    suma = sum(H[i,:])
    #    H[i,:] /= suma
    #    H[:,i] /= suma
    return Qobj(H)

    #! .unit quizá funciona. Comprobarlo 


def Liouvillian(alpha, PI_ij, H):
    n_nodes = len(PI_ij)
    _Liouvillian = -1j*(1-alpha)*(spre(H)-spost(H))
    for i in range(n_nodes):
        for j in range(n_nodes):
            _Liouvillian += alpha * PI_ij[j][i] * lindblad_dissipator(L_ij(i,j,n_nodes))
    return _Liouvillian

if __name__=='__main__':
    A_ij = np.zeros([2,2])
    A_ij[0,1] = 4
    A_ij[1,0] = 5
    A_ij = convert_to_list(A_ij)
    g_ij = calculate_G(A_ij)
    print_matrix(g_ij)
    #for s in ['mean','max','min','norm','diff']:
    #    h = Hamiltonian(g_ij, style=s)
    #    print(s, -h[1,0]*h[0,1])