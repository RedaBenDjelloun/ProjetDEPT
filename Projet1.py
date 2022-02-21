import random                       ## Générer des coordonnées aléatoires pour les clients et les sites potentiels
import time                         ## Obtenir une graine pour random
import numpy as np                  ## Opérations de matrices
import matplotlib.pyplot as plt

## Initialisation de np.random
rnd = np.random
rnd.seed(time.gmtime())

## Initialisation aléatoire des clients et des sites
n = 5 # Nombre de clients
xc = rnd.rand(n) * 200
yc = rnd.rand(n) * 100

m = 3  # Nombre de sites potentiels
xf = rnd.rand(m) * 200
yf = rnd.rand(m) * 100

## Graphe initial des clients et des sites potentiels
plt.scatter(xc[0:], yc[0:], c='b', label = 'Customer')              # Customer
plt.scatter(xf[0:], yf[0:], c='r', marker='s', label = 'Facility')  # Facility
plt.legend()
plt.show()

## Construction de la fonction de coût (Cas Uncapacitated)
I = [i for i in range(0, n)]            # Clients
J = [i for i in range(0, m)]            # Sites potentiels
h = {i: rnd.randint(1, 10) for i in I}  # Demande des clients, aléatoire
A = [(i, j) for i in I for j in J]      # 2-D cartesian product
f = {j: 100 for j in J}                 # Fixed setup cost of Facility
c = {(i, j): 1*np.hypot(xc[i]-xf[j], yc[i]-yf[j]) for (i, j) in A} # Cost to reach customer from Facility

from gurobipy import Model, GRB, quicksum ## Solveur
mdl = Model('UFLP');

x = mdl.addVars(J, vtype = GRB.BINARY)
y = mdl.addVars(A, vtype = GRB.CONTINUOUS)

mdl.ModelSense = GRB.MINIMIZE # Minimisation model
mdl.setObjective(quicksum(f[j]*x[j] for j in J) + quicksum(h[i]*c[i,j]*y[i,j] for i,j in A))
# Building cost + Routing cost (h[i]*y[i,j] est la fraction de demande du client i produite dans le centre j)

mdl.addConstrs(quicksum(y[i,j] for j in J) == 1 for i in I);
mdl.addConstrs(y[i,j] <= x[j] for i,j in A);

mdl.optimize() # Solution cost: 5180.93 (varies with changing seed value)









