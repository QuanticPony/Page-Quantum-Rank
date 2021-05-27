#%%
import numpy as np

from qutip.steadystate import steadystate

from funciones import *

from pyvis.network import Network


from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib import cm

import pickle

import networkx as nx
import matplotlib.pyplot as plt


N_samples = 20
alpha_range = np.linspace(0.1,1,N_samples)

styles = ['mean','max','min','norm','diff']

N_nodos = 40

#%%
normal_rank = {}
quantum_rank = {}
google_rank = {}

for style in styles:
    
    normal_rank.update({style:[]})
    quantum_rank.update({style:[]})
    google_rank.update({style:[]})
    
    for alpha in alpha_range:
        with open(f'h/{style}/datos_{alpha:.02f}.dat', 'rb') as file:
            PR, QR, GR, names = pickle.load(file)
        normal_rank[style].append(PR)
        quantum_rank[style].append(QR)
        google_rank[style].append(GR)
        
#%%
        
serie = np.zeros(N_samples)  
params = {"ytick.color" : "w",
          "xtick.color" : "w",
          "axes.labelcolor" : "w",
          "axes.edgecolor" : "w"}
plt.rcParams.update(params)

for style in styles:
    fig, ax = plt.subplots()
    
    ax.grid()
    
    style_types = {
        'mean': r'$(g_{ij}+g_{ji})/2$',
        'max': r'$max(g_{ij},g_{ji})$',
        'min': r'$min(g_{ij},g_{ji})$',
        'norm': r'$\sqrt{g_{ij}^2+g_{ji}^2}$',
        'diff': r'$|g_{ij}-g_{ji}|$',
    }
    
    ax.set_title(f"Hamiltonian: {style_types[style]}", color="w")
    ax.set_xlabel(r'$\alpha$')
    ax.set_ylabel('Quantum Rank')
    
    ax.set_ylim(0,0.16)
    ax.set_xlim(0.1,1)
    norm = colors.Normalize(vmin=min(normal_rank[style][0]), vmax=max(normal_rank[style][0]))
    cmap = cm.get_cmap('rainbow')
    
    def color(value):
        rgb = cmap(norm(abs(value)))[:3]
        color = colors.rgb2hex(rgb)
        return color
    
    for i in range(N_nodos):
        for j, alpha in enumerate(alpha_range):
            serie[j] = quantum_rank[style][j][i]
        ax.plot(alpha_range, serie, color=color(normal_rank[style][0][i]))
    fig.savefig(f'{style}.png', transparent=True)