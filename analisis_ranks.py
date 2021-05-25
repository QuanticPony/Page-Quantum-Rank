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
axin = np.zeros(NNN-1)
axout = np.zeros(NNN-1)



# for i in range(2,20):
    
    
    
#     plt.hist(Grado_in, bins=i)
#     plt.show()

def do(g, title):
    hist, arange = np.histogram(g, 20)
    arange += arange[1]*0.5

    hist = hist/sum(hist)
    hist_only = []
    arange_only = []
    for i, h in enumerate(hist):
        if h!=0:
            hist_only.append(h)
            arange_only.append(arange[i] + 0.5* arange[1])

    def _pow(x,m,n):
        return n*x**m

    popti,pcovi = curve_fit(_pow, arange_only, hist_only)
    # plt.xscale('log')
    # plt.yscale('log')
    plt.ylim(0,0.8)
    plt.xlabel('Grado de nodo')
    plt.ylabel(r'$P_{k}$')
    plt.title(title)
    plt.bar(arange_only, hist_only, arange[1])
    plt.plot(np.linspace(20,900,50), _pow(np.linspace(0,900,50), *popti), label='$P(k)\propto k^{'+f'{popti[0]:.2f}'+'}$', c='r')
    plt.legend()
    plt.grid()
    plt.show()


do(Grado_in, "Distribución de grado 'in'")
do(Grado_out, "Distribución de grado 'out'")
#%%

# for gin, gout in zip(Grado_in, Grado_out):
#     P_grado_in[int(np.floor(gin/delta_in))] += 1
#     P_grado_out[int(np.floor(gout/delta_out))] += 1
#     axin[int(np.floor(gin/delta_in))] += gin
#     axout[int(np.floor(gout/delta_out))] += gout

# axin /= P_grado_in
# axout /= P_grado_out

# P_grado_in /= sum(P_grado_in)
# P_grado_out /= sum(P_grado_out)

# in_range = range_in[:-1]+delta_in/2
# out_range = range_out[:-1]+delta_out/2
    
# xin = range_in[:-1]+delta_in/2
# xout = range_out[:-1]+delta_out/2


# ax2.scatter(axin , P_grado_in)
# ax2.scatter(axout , P_grado_out)
# ax2.set_yscale('log')
# ax2.set_xscale('log')

# ax2.set_xlabel('Grado de nodo')
# ax2.set_ylabel(r'$P_{k}$')


# #plt.scatter(np.arange(41), Grado_in)
# #plt.scatter(np.arange(41), Grado_out)


# def _pow(x,m,n):
#     return n*x**m

# popti,pcovi = curve_fit(_pow,axin,P_grado_in)
# popto,pcovo = curve_fit(_pow,axout,P_grado_out)

# ax2.plot(axin,_pow(axin,*popti),label='$P(k)\propto k^{'+f'{popti[0]:.2f}'+'}$')
# ax2.plot(axout,_pow(axout,*popto),label='$P(k)\propto k^{'+f'{popto[0]:.2f}'+'}$')
# ax2.legend()


# xticks = [100,200,300,400,600]
# ax2.set_xticks(xticks)
# ax2.set_xticklabels(["$%.1f$" % x for x in xticks])
# yticks = [0.05,0.1,0.2,0.3,0.5,0.7,1]
# ax2.set_yticks(yticks)
# ax2.set_yticklabels(["$%.2f$" % y for y in yticks])


# ax2.set_xlabel('k')
# ax2.set_ylabel('P(k)')
# ax2.set_title('Distribución de grado')
# ax2.grid()
# plt.show()

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

#nx.draw(FisCord)
#plt.show()
# %%

# fig4, ax4=plt.subplots()
# a=list(hist.keys())
# b=list(hist.items())
# ax4.scatter(a,b)

# plt.show()
# %%
