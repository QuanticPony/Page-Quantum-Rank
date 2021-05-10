#%%
import numpy as np
from collections import defaultdict

print('Hola Mundo')

def read_links(filename, n_nodes):
    '''
    Reads a file and returns the adjacency matrix
    '''
    cero = lambda : 0
    A_ij = [defaultdict(cero) for _ in range(n_nodes)]

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

def calculate_PI(a_ij):
    '''
    Given the adjacency matrix returns the transition matrix
    '''
    n_nodes = len(a_ij)
    cero = lambda : 0
    PI_ij = [defaultdict(cero) for _ in range(n_nodes)]
    
    for i, ai in enumerate(a_ij):
        PI_ij[i].update(ai.copy())
        
        out_grade = sum(ai.values())
        for j in PI_ij[i].keys():
            PI_ij[i][j] /= out_grade    
    return PI_ij

def evolve(P, PI_ij):
    '''
    Evolves the system a temporal discrete step using the transition matrix
    '''
    Pnew=np.zeros(len(P))
    for i in range(len(P)):
        for j in range(len(P)):
            Pnew[i] += P[j] * PI_ij[j][i]
    return Pnew     

def evolveG(P, PI_ij, q=0.9):
    '''
    Evolves the system a temporal discrete step using the Google matrix
    '''
    F = (1-q)/(len(P)-1)
    Pnew=np.zeros(len(P))
    for i in range(len(P)):
        for j in range(len(P)):
            Pnew[i] += P[j] * (q * PI_ij[j][i]+ (i!=j)*F)
    return Pnew     
    
    
def equal(P1,P2, delta):
    '''
    Returns `True` if all the components in `P1` and `P2` are closer than `delta`. Else returns `False`
    '''
    for i,j in zip(P1,P2):
        if abs(i-j)>delta:
            return False      
    return True


def print_rank(P):
    '''
    Prints out via terminal the nodes and the page rank given `P`
    '''
    print('Pagerank:')
    t = np.argsort(P)[::-1]
    for i in t:
        print(i+1, P[i])
        

if __name__=='__main__':
    A_ij = read_links('simple-net.txt', 8)
    PI_ij = calculate_PI(A_ij)
    
    P = np.zeros(8)
    P[0]=1
    for _ in range(1000):
        Pnew = evolve(P, PI_ij)
        if equal(P, Pnew, 0.0001):
            break
        P = evolve(Pnew, PI_ij)
        #print(P)
    P=P/sum(P)
    print_rank(P)
        
        
    print('_________________________')
    
    P = np.zeros(8)
    P[0]=1
    for _ in range(1000):
        Pnew = evolveG(P, PI_ij)
        if equal(P, Pnew, 0.0001):
            break
        P = evolveG(Pnew, PI_ij)
        #print(P)
    P=P/sum(P)
    print_rank(P)
        
    print('_________________________')

    #matriz = np.zeros([8,8])
    #q=0.6
    #F = (1-q)/(len(P)-1)
    #for i in range(8):
    #   for j in range(8):
    #       matriz[i,j] = q * PI_ij[i][j]+ (i!=j)*F
    #avec, aval = np.linalg.eig(matriz)

    #print(avec)
    
    #print('pato')