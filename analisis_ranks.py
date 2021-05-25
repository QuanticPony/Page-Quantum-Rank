#%%
import numpy as np

from qutip.steadystate import steadystate

from funciones import *

from pyvis.network import Network

from matplotlib import pyplot as plt

import pickle

import networkx as nx

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
    
xin = range_in[:-1]+delta_in/2
xout = range_out[:-1]+delta_out/2

plt.scatter(xin , P_grado_in)
plt.scatter(xout , P_grado_out)
plt.yscale('log')
plt.xscale('log')


# %%
#plt.scatter(np.arange(41), Grado_in)
#plt.scatter(np.arange(41), Grado_out)
# %%

def pow(x,m,n):
    return n*x**m

popti,pcovi = curve_fit(pow,xin,P_grado_in)
popto,pcovo = curve_fit(pow,xout,P_grado_out)

plt.plot(xin,pow(xin,*popti),label='$P(k)\propto k^{'+f'{popti[0]:.2f}'+'}$')
plt.plot(xout,pow(xout,*popto),label='$P(k)\propto k^{'+f'{popto[0]:.2f}'+'}$')
plt.legend()
plt.xlabel('k')
plt.ylabel('P(k)')
plt.title('Distribución de grado')
plt.grid()
plt.show()

FisCord = nx.DiGraph()
lista_Red = []
for j,column in enumerate(A_ij):
   for elto in column.keys():
       lista_Red.append((names[elto+1], names[j+1], A_ij[j][elto]))
FisCord.add_weighted_edges_from(lista_Red)

# plt.subplot(121)
# nx.draw(FisCord, with_labels=True, font_weight='bold')
# plt.subplot(122)
# nx.draw_shell(FisCord, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
# plt.show()
FC_clustering=nx.clustering(FisCord)
cluster=sum(FC_clustering.values())/len(FC_clustering.values())
print(f"clustering: {cluster:.4}")
pearson=nx.degree_pearson_correlation_coefficient(FisCord)
print(f"asortatividad (r): {pearson:.4}")


#%%

degree_sequence = [d for n, d in FisCord.degree()]  # degree sequence
print(f"Degree sequence {degree_sequence}")
print("Degree histogram")
hist = {}
for d in degree_sequence:
    if d in hist:
        hist[d] += 1
    else:
        hist[d] = 1
print("degree #nodes")
for d in hist:
    print(f"{d:4} {hist[d]:6}")

nx.draw(FisCord)
plt.show()
# %%

plt.clf()
fig2, ax2=plt.subplots()

ax2.plot(hist.keys(),hist.items(),'.')

plt.show()
# %%
