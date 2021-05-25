#%%
import numpy as np

from qutip.steadystate import steadystate

from funciones import *

from pyvis.network import Network


from matplotlib import pyplot as plt

import pickle

import networkx as nx
import matplotlib.pyplot as plt


N_samples = 51
alpha_range = np.linspace(0,1,N_samples)
styles = ['mean','max','min','norm','diff']

N_nodos = 41

#%%
normal_rank = {}
quantum_rank = {}
google_rank = {}

for style in styles:
    
    normal_rank.update({style:[]})
    quantum_rank.update({style:[]})
    google_rank.update({style:[]})
    
    for alpha in alpha_range:
        with open(f'{style}/datos_{alpha:.02f}.dat', 'rb') as file:
            PR, QR, GR, names = pickle.load(file)
        normal_rank[style].append(PR)
        quantum_rank[style].append(QR)
        google_rank[style].append(GR)
        
#%%
        
serie = np.zeros(N_samples)  

for style in styles:
    fig, ax = plt.subplots()
    
    ax.set_title(style)
    ax.set_xlabel(r'$\alpha$')
    ax.set_ylabel('QR')
    
    ax.set_ylim(0,0.2)
    ax.set_xlim(0.1,1)
    
    for i in range(N_nodos):
        for j, alpha in enumerate(alpha_range):
            serie[j] = quantum_rank[style][j][i]
        ax.plot(alpha_range, serie)
        
plt.show()