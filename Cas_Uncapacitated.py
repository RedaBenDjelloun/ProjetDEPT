###
import time

import gurobipy
import matplotlib.pyplot as plt
import numpy as np

rnd = np.random
rnd.seed(time.gmtime())

d = 10  # Nombre de clients (les villes)

xc = rnd.rand(d) * 200  # x-coordinate
yc = rnd.rand(d) * 100  # y-coordinate

s = 20  # Nombre de sites potentiels

xf = rnd.rand(s) * 200  # x-coordiante
yf = rnd.rand(s) * 100  # y-coordiante

# Les coordonnées sont aléatoires on associera le modèle à la réalité à travers les coûts de transport et
# on essaiera de les mettre sur la carte ?
def uncap1():
    plt.scatter(xc[0:], yc[0:], c='b', label='Clients')  # Clients
    plt.scatter(xf[0:], yf[0:], c='r', marker='s', label='Sites potentiels')  # Facility
    plt.legend()
    plt.show()

# On affiche les clients (en bleu) et les sites potentiels (en rouge)

# Coordonnées des sites potentiels

Si = (np.pi / 180) * np.array(
    [[45.77754586288763, 4.706226], [47.42848880083095, 0.696609939732838], [49.429128383215385, 2.8572368091341276],
     [49.147213627674724, 0.27351229808086314], [48.79528370580836, 2.4329536128064353],
     [43.603090659038905, 2.236904420668811], [44.21013227868792, 5.928072354942097],
     [43.905075190292116, 4.702242610956951], [47.930994317041744, -2.367834904424218
                                               ], [45.64608237636729, 3.702192431239796],
     [43.59416822165148, 1.391004283885082], [47.35264577586803, 1.1954343821942992],
     [45.13872767315636, 5.693890835423045], [49.000127015386994, 1.1389370532938559],
     [43.69844732023985, 0.07642417400895661], [46.21899620573784, -0.13396661613968203],
     [47.286737799412606, 5.0125235973982365], [45.79494666942314, 3.116056470833112],
     [44.60875495330718, 4.40021943009235]])

# Coordonnées des clients

V = (np.pi / 180) * np.array([[48.863372198251085, 2.3353620272200293], [43.30033735022251, 5.403307650102295],
                              [45.755555316490565, 4.833413486228247], [43.59821698096177, 1.4362756775435046],
                              [43.7141149602082, 7.242512267369487], [47.225877035701515, -1.5431683622824774],
                              [43.606535933402775, 3.872796058982598], [48.57770659339895, 7.764139236526103],
                              [44.85106259456057, -0.567129298510725], [50.62999171999595, 3.0709303928045317]])

# Matrice des distances

Delta = np.zeros((len(Si), len(V)))
for s in range(len(Si)):
    for i in range(len(V)):
        phiA = Si[s][0]
        lambdaA = Si[s][1]
        phiB = V[i][0]
        lambdaB = V[i][1]
        Dlambda = lambdaB - lambdaA
        Delta[s][i] = (6378137 / 1000) * np.arccos(
            np.sin(phiA) * np.sin(phiB) + np.cos(phiA) * np.cos(phiB) * np.cos(Dlambda))

D = [i for i in range(d)] #Clients

S = [i for i in range(s)] #Sites potentiels
h = {d: 100000 for d in D}
A = [(d, s) for d in D for s in S]  # 2-D cartesian product
f = {s: 100 for s in S}
delta = {(d, s): 0.05 * Delta[s, d] for (d, s) in A}  # Cost to reach customer from Facility

from gurobipy import Model, GRB, quicksum

mdl = gurobipy.Model('UFLP')

#Déclaration des variables
x = mdl.addVars(S, vtype=GRB.BINARY)
y = mdl.addVars(A, vtype=GRB.CONTINUOUS)
q = mdl.addVars(A, vtype=GRB.CONTINUOUS)

#Fonction objectif
mdl.ModelSense = GRB.MINIMIZE # Minimisation model
mdl.setObjective(quicksum(f[s]*x[s] for s in S) + quicksum(h[d]*delta[d,s]*y[d,s] for d,s in A)) + quicksum(q[d,s] for d,s in A) # Cost Function

#Différentes contraintes
mdl.addConstrs(quicksum(y[d,s] for s in S) <= s for d in D)
mdl.addConstrs(y[d,s] <= x[d] for d,s in A)
mdl.addConstrs(quicksum(q[d,s] for s in S) == h[d] for d in D)

mdl.optimize()


assignment = [a for a in A if y[a].X > 0.0]

#Permet de plot la carte dans le main
def uncap2():
    for i, j in assignment:
        plt.plot([xc[i], xf[j]], [yc[i], yf[j]], c='g', zorder=0)
    plt.scatter(xc[0:], yc[0:], c='b', label='Clients')
    plt.scatter(xf[0:], yf[0:], c='r', marker='s', label='Sites potentiels')
    plt.legend()
    plt.show()