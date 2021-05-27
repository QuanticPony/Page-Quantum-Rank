import numpy as np

from qutip.steadystate import steadystate

from funciones import *

import pickle

if __name__=='__main__':
    
    n_nodes=41
    A_ij = read_links('links-sin-bots.txt', n_nodes)

    # Leemos correspondencia entre nombre y nodo del archivo de texto y lo guardamos en un diccionario
    with open('correspondencia_final.txt', encoding='latin-1', errors='replace') as corr:
        names = {}
        for line in corr:
            node, name = line.split(maxsplit=1)
            node = int(node)
            name = name[0:-1]
            names.update({node: name})
    
    PI_ij = calculate_PI(A_ij)
    G_ij = calculate_G(PI_ij, 0.9)
    
    # alpha_range = np.linspace(0.1,1,20)
    alpha_range = [0.9]
    for style in ['mean']:#,'max','min','norm','diff']:
        H = Hamiltonian(G_ij, style=style)
        
        GR = page_rank(A_ij, evolveG, equal)
        GR = np.array(GR)
        PR = page_rank(A_ij, evolve, equal)
        PR = np.array(PR)
                
        for alpha in alpha_range:
            time_in = time()*1e-6
            # print(f'Valor de alpha: {alpha:.2f}')
            
            L = Liouvillian(alpha, G_ij, H)
    
            QR = np.zeros(n_nodes)
            p = steadystate(L)
            for i in range(n_nodes):
                QR[i] = np.real(p[i,i])
            print(f"Tiempo transcurrido: {(time()*1e-6-time_in)}ms")
    
            with open(f'{style}/datos_{alpha:.02f}.dat', 'wb') as file:
                pickle.dump([PR, QR, GR, names], file)

        print(style)
        print('#################################################################')
        print('Google')
        print_rank(GR, names=names)
        print('#################################################################')
        print(r'Cuantica con $\alpha$' + f'={alpha_range}')
        print_rank(QR, names=names)
        print('#################################################################')
    if len(alpha_range)==1:
        with open('datos.dat', 'wb') as file:
            pickle.dump([PR, QR, GR, names], file)
