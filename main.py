#%%
from numba.np.ufunc import parallel
import numpy as np
from collections import defaultdict
from time import time_ns as time

from numba import jit

from funciones import *
        

if __name__=='__main__':
    A_ij = read_links('simple-net.txt', 8)
    PI_ij = calculate_PI(A_ij)
    
    print('*************************')
    page_rank(A_ij, evolve, equal)
    
    print('*************************')
    page_rank(A_ij, evolve_T, equal, _transpuesta=True)
    print('*************************')
    
    page_rank(A_ij, evolveG, equal)
    print('*************************')
    
    #P = np.zeros(8)
    #P[0]=1
    #time_in = time()
    #for _ in range(1000):
    #    Pnew = evolveG(P, PI_ij)
    #    if equal(P, Pnew, 0.0001):
    #        break
    #    P = evolveG(Pnew, PI_ij)
    #    #print(P)
    #print(time()-time_in)
    #P=P/sum(P)
    #print_rank(P)
    #    
    #print('_________________________')

    #matriz = np.zeros([8,8])
    #q=0.6
    #F = (1-q)/(len(P)-1)
    #for i in range(8):
    #   for j in range(8):
    #       matriz[i,j] = q * PI_ij[i][j]+ (i!=j)*F
    #avec, aval = np.linalg.eig(matriz)

    #print(avec)
    
    #print('pato')