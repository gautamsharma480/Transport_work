import numpy as np
import matplotlib.pyplot as plt
from matplotlib import re
# This script generates the typical behaviour of Seebeck Coefficient. 
# Fig. 1b (Selection function vs mu plot) from Applied Physics Reviews 5, 021303 (2018); doi: 10.1063/1.5021094
kB = 1.38e-23 # J/K
eV = 1.60218e-19 #J
def cb(x): # Not used
    Ecb = [2*i**2 + 2 for i in x]
    return Ecb
def vb(x):   # Not used
    Evb = [-2*i**2 - 2 for i in x]
    return Evb
def seebeck(Ef,E,T):  # Not used
    S = [(i-Ef)/kB*T for i in E]
    return S

def FD(E,Ef,T):   # Not used
    f = 1/((np.exp(E-Ef)/kB*T) -1)
    return f

def dfde(E,Ef,T):
    E=E*eV # Converting Joule to eV
    Numerator = -np.exp((E-Ef)/(kB*T))
    Denominator = (1 + np.exp((E-Ef)/(kB*T)))**2
    dfde = Numerator/Denominator
    return dfde

mu=np.arange(-0.5,0.5,0.01)
Ef = 0.0

Seeb_300=[]
Seeb_400=[]
Seeb_500=[]
for i in mu:
    y_300 = (i - Ef) * dfde(i, Ef,300)
    y_400 = (i - Ef) * dfde(i, Ef, 400)
    y_500 = (i - Ef) * dfde(i, Ef, 500)
    Seeb_300.append(y_300)
    Seeb_400.append(y_400)
    Seeb_500.append(y_500)

plt.plot(mu,Seeb_300,marker='s',label='T = 300 K')
plt.plot(mu,Seeb_400, marker = 'o',label='T = 400 K')
plt.plot(mu,Seeb_500, marker = 'p',label='T = 500 K')
plt.axvline(x=0)
plt.axhline(y=0)
plt.xlabel(r'$\mu$ (eV)', fontsize=16)
plt.ylabel(r'$\mu*\partial f/\partial E$ (eV)', fontsize=16)
plt.legend()
plt.show()
