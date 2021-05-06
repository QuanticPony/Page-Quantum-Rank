#%%
import numpy as np
from collections import defaultdict



def read_links(filename, n_nodes):
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
    n_nodes = len(a_ij)
    cero = lambda : 0
    PI_ij = [defaultdict(cero) for _ in range(n_nodes)]
    
    for i, ai in enumerate(a_ij):
        PI_ij[i].update(ai.copy())
        
        out_grade = sum(ai.values())
        for j in PI_ij[i].keys():
            PI_ij[i][j] /= out_grade
            #PI_ij[i].update({j:PI_ij[i][j]/out_grade})
            
    return PI_ij


def evolve(P, PI_ij):
    Pnew=np.zeros(len(P))
    for i in range(len(P)):
        for j in range(len(P)):
            Pnew[i] += P[j] * PI_ij[i][j]
    return Pnew     

def evolveG(P, PI_ij, q=0.9):
    F = (1-q)/(len(P)-1)
    Pnew=np.zeros(len(P))
    for i in range(len(P)):
        for j in range(len(P)):
            Pnew[i] += P[j] * (q * PI_ij[i][j]+ (i!=j)*F)
    return Pnew     
    
    #for i, PIi in enumerate(G_ij):
    #    for j in PIi.keys():
    #        Pnew[i] += PIi[j]*P[j]
    

if __name__=='__main__':
    A_ij = read_links('simple-net.txt', 8)
    PI_ij = calculate_PI(A_ij)
    
    P = np.zeros(8)
    P[0]=1
    for _ in range(100):
        P = evolve(P, PI_ij)
        #print(P)
    P=P/sum(P)
    #print(P)
    

    matriz = np.zeros([8,8])
    q=0.6
    F = (1-q)/(len(P)-1)
    for i in range(8):
       for j in range(8):
           matriz[i,j] = q * PI_ij[i][j]+ (i!=j)*F
    avec, aval = np.linalg.eig(matriz)

    print(avec)
    
    #print('pato')
# %%
