#%%
import numpy as np
from collections import defaultdict

from funciones import *
        



if __name__=='__main__':
    A_ij = read_links('simple-net.txt', 8)
    H_ij = convert_to_matrix(A_ij)
    
    print_matrix(H_ij)
            
    
    #print('*************************')
    #page_rank(A_ij, evolve, equal)
    #
    ##print('*************************')
    ##page_rank(A_ij, evolve_T, equal, _transpuesta=True)
    #print('*************************')
    #
    #page_rank(A_ij, evolveG, equal)
    #print('*************************')