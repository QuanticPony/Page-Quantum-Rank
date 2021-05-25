#%%
import numpy as np

from qutip.steadystate import steadystate

from funciones import *

from pyvis.network import Network

from matplotlib import pyplot as plt

import pickle


with open('datos.dat', 'rb') as file:
    PR, QR, GR = pickle.load(file)
    
    plt.style.use('fast')
    
    p_PR = np.argsort(PR)[::-1]
    p_QR = np.argsort(QR)[::-1]
    p_GR = np.argsort(GR)[::-1]
    
with open('correspondencia.txt',encoding='latin-1', errors='replace') as corr:
   names = {}
   for line in corr:
       node, name = line.split(maxsplit=1)
       node = int(node)
       name = name[0:-1] # El replace no me funcionaba, con esto sí que me quita el \n
       names.update({node: name})
       
       
#for j,[pi,gi,qi] in enumerate(zip(p_PR, p_GR, p_QR)):
#    #print(f'{j+1})', names[pi+1], f"{PR[pi]:.6}\t{GR[qi]:.6}\t{QR[gi]:.6}")
#    print(f'{j+1})', names[pi+1],  names[gi+1], names[qi+1])
    
#print(p_PR)
#print(p_GR)
#print(p_QR)


plt.scatter(np.arange(0,41), p_QR-p_PR)
#plt.scatter(np.arange(0,41), GR)
#plt.scatter(np.arange(0,41), GR)

#plt.scatter(np.arange(0,40), p_QR)
#plt.scatter(np.arange(0,40), p_GR)

plt.xlabel('Posición PR')
plt.ylabel('(Posición QR) - (Posición PR)')



A_ij = read_links('links-sin-bots.txt', 41)
TA_ij = transpuesta(A_ij)


Grado_in = np.zeros(41)
Grado_out = np.zeros(41)
for i, ai in enumerate(A_ij):
    Grado_out[i] = sum(ai.values())
for i, tai in enumerate(TA_ij):
    Grado_in[i] = sum(tai.values())
    
P_grado_in = Grado_in / sum(Grado_in)
P_grado_out = Grado_out / sum(Grado_out)

plt.show()
#%%
NNN = 4

range_in = np.linspace(0,max(Grado_in)+0.001, NNN)
delta_in = range_in[1]-range_in[0]
range_out = np.linspace(0,max(Grado_out)+0.001, NNN)
delta_out = range_out[1]-range_out[0]

P_grado_in = np.zeros(NNN-1)
P_grado_out = np.zeros(NNN-1)
for gin, gout in zip(Grado_in, Grado_out):
    P_grado_in[int(np.floor(gin/delta_in))] += 1
    P_grado_out[int(np.floor(gout/delta_out))] += 1
    
P_grado_in /= sum(P_grado_in)
P_grado_out /= sum(P_grado_out)
    
plt.scatter(range_in[:-1]+delta_in/2, P_grado_in)
plt.scatter(range_out[:-1]+delta_out/2, P_grado_out)
plt.yscale('log')
plt.xscale('log')


# %%
plt.scatter(np.arange(41), Grado_in)
plt.scatter(np.arange(41), Grado_out)
# %%

def linear(x,m,n):
    pass