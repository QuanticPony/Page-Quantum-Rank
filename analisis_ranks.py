#%%
import numpy as np

from qutip.steadystate import steadystate

from funciones import *

from pyvis.network import Network

from matplotlib import pyplot as plt

import pickle

from scipy.optimize import curve_fit


with open('datos.dat', 'rb') as file:
    PR, QR, GR, names = pickle.load(file)
    
    plt.style.use('fast')
    
    p_PR = np.argsort(PR)[::-1]
    p_QR = np.argsort(QR)[::-1]
    p_GR = np.argsort(GR)[::-1]
       
#for j,[pi,gi,qi] in enumerate(zip(p_PR, p_GR, p_QR)):
#    #print(f'{j+1})', names[pi+1], f"{PR[pi]:.6}\t{GR[qi]:.6}\t{QR[gi]:.6}")
#    print(f'{j+1})', names[pi+1],  names[gi+1], names[qi+1])

    
#print(p_PR)
#print(p_GR)
#print(p_QR)

#%%

#plt.scatter(np.arange(0,41), p_QR-p_PR)

diff = np.zeros(41)
for i, pg in enumerate(p_GR):
    p_QR: np.ndarray
    for j, pq in enumerate(p_QR):
        if pg == pq:
            diff[i] = j-i
    
fig1, ax1 = plt.subplots()

ax1.scatter(np.arange(0,41), diff)

# plt.scatter(np.arange(0,41), GR[p_GR])
# plt.scatter(np.arange(0,41), QR[p_QR])

#plt.scatter(np.arange(0,41), GR)
#plt.scatter(np.arange(0,41), GR)
ax1.grid()
ax1.set_xlabel('Posición PR')
ax1.set_ylabel('(Posición QR) - (Posición PR)')

plt.show()


#%%

fig2, ax2 = plt.subplots()

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


def exponential(x, m, n):
    return pow(x, m) + n

popt_in, pcov_in = curve_fit(exponential, range_in[:-1]+delta_in/2, P_grado_in, p0=[-3,0])
popt_out, pcov_out = curve_fit(exponential, range_out[:-1]+delta_out/2, P_grado_out, p0=[-3,0])

in_range = range_in[:-1]+delta_in/2
out_range = range_out[:-1]+delta_out/2
    
ax2.scatter(in_range, P_grado_in)
ax2.scatter(out_range, P_grado_out)

ax2.plot(in_range, exponential(in_range, *popt_in))
ax2.plot(out_range, exponential(out_range, *popt_out))

ax2.set_yscale('log')
ax2.set_xscale('log')

ax2.set_ylim(1e-2,1)
ax2.set_xlim(1e2, 8e2)

ax2.set_xlabel('Grado de nodo')
ax2.set_ylabel(r'$P_{k}$')

#%%
ax2.scatter(np.arange(41), Grado_in)
ax2.scatter(np.arange(41), Grado_out)


#%%

