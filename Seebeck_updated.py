import numpy as np
import matplotlib.pyplot as plt
from matplotlib import re
kB = 1.38e-23 # J/K
eV = 1.60218e-19 #J
def cb(x): # Not used
    Ecb = [2*i**2 + 2 for i in x]
    return Ecb
def vb(x):  # Not used
    Evb = [-2*i**2 - 2 for i in x]
    return Evb
def seebeck(E,Ef,T): # Not used
    S = [(i-Ef)/(kB*T) for i in E]
    return S

def FD(E,Ef,T): 
    E = E*eV
    f = 1/(np.exp((E-Ef)/(kB*T)) + 1)
    return f

def dfde(E,Ef,T): 
    E=E*eV # Converting Joule to eV
    Numerator = -np.exp((E-Ef)/(kB*T))
    Denominator = (1 + np.exp((E-Ef)/(kB*T)))**2
    dfde = Numerator/Denominator
    return dfde

mu=np.arange(-0.5,0.5,0.01)
Ef = 0.0

def plot_mu_dfde(): # plots selection function for T=300,400,500 K.
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

def plot_FD(): # plots Fermi-Dirac distribution for T=300,400,500 K.
    FD_300=[]
    FD_400=[]
    FD_500=[]

    for i in mu:
        y_300 = FD(i, Ef,300)
        y_400 = FD(i, Ef, 400)
        y_500 = FD(i, Ef, 500)
        FD_300.append(y_300)
        FD_400.append(y_400)
        FD_500.append(y_500)
    plt.plot(mu,FD_300,marker='s',label='T = 300 K')
    plt.plot(mu,FD_400, marker = 'o',label='T = 400 K')
    plt.plot(mu,FD_500, marker = 'p',label='T = 500 K')
    plt.axvline(x=0)
    plt.axhline(y=0)
    plt.xlabel(r'$\mu$ (eV)', fontsize=16)
    plt.ylabel('Fermi Occupation', fontsize=16)
    plt.legend()

def plot_dfde(): # plots negative of derivative of Fermi-Dirac distribution for T=300,400,500 K.
    dfde_300=[]
    dfde_400=[]
    dfde_500=[]
    for i in mu:
        y_300 = -dfde(i, Ef,300)
        y_400 = -dfde(i, Ef, 400)
        y_500 = -dfde(i, Ef, 500)
        dfde_300.append(y_300)
        dfde_400.append(y_400)
        dfde_500.append(y_500)
    plt.plot(mu,dfde_300,marker='s',label='T = 300 K')
    plt.plot(mu,dfde_400, marker = 'o',label='T = 400 K')
    plt.plot(mu,dfde_500, marker = 'p',label='T = 500 K')
    plt.axvline(x=0)
    plt.axhline(y=0)
    plt.xlabel(r'$\mu$ (eV)', fontsize=16)
    plt.ylabel(r'-$\partial f/\partial E$ (eV)', fontsize=16)
    plt.legend()
#plot_FD()
plot_mu_dfde()
#plot_dfde()
plt.show()
