###
import random
import time
import numpy as np
import matplotlib.pyplot as plt
rnd = np.random
rnd.seed(time.gmtime())

I = 20 # Nombre de clients
xc = rnd.rand(I) * 200 # x-coordinate
yc = rnd.rand(I) * 100 # y-coordinate

S = 10  # Numebr of Facility
xf = rnd.rand(S) * 200 # x-coordiante
yf = rnd.rand(S) * 100 # y-coordiante

plt.scatter(xc[0:], yc[0:], c='b', label = 'Customer') # Customer
plt.scatter(xf[0:], yf[0:], c='r', marker='s', label = 'Facility') # Facility
plt.legend()
plt.show()

print("Bonjour Sohalia")
print("Bonjour Valentine")



