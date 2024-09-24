#!/usr/bin/env  python3
import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
import sys

prefix = sys.argv[1]
ry2ev = 13.605698066
bohr2angs = 0.529177249
ev2ry = 1 / ry2ev

trace = np.loadtxt(prefix + '.condtens')
kl = np.loadtxt('kappa.txt')
for i in range(0, 4):
    print(kl[i, 0], kl[i][1])

f = open(prefix + '.nscf.out', 'r')
f_pw = f.readlines()
f.close()
shift_gap = 0

for line in f_pw:

    if 'unit-cell' in line:
        vol = float(line.split()[3]) * (bohr2angs ** 3) * 1e-24
    if 'highest occupied, lowest unoccupied level' in line:
        if shift_gap == 0:
            VBM = float(line.split()[6])
            CBM = float(line.split()[7])
            Fermi = (VBM + CBM) * 0.5
            # print('Fermi=', Fermi,'eV' )
    if 'Fermi' in line:
        Fermi = float(line.split()[4])
print('Fermi=', Fermi, 'eV')


# print(trace.shape)

def prn(x, n):  ## printing nn number of digits after decimal
    if n == 3:
        xx = '%1.2e' % x
    else:
        xx = '%.5f' % x
    return xx


def closest(lst, K):
    lst = np.asarray(lst)
    idx = (np.abs(lst - K)).argmin()
    return idx


cc = []
for i in range(0, trace.shape[0]):
    cc.append(trace[i, 0])

index = closest(cc, Fermi * ev2ry)
print('index', index)
print("Fermi=", trace[index, 0], ", Nf=", trace[index, 2])

"Fermi is subtracted : "
trace[:, 0] -= trace[index, 0]  # E-Ef # its in Ry here

# trace[:,2] -= trace[index,2]  # N-Nf
print('Nf not subtracted')

trace[:, 0] *= ry2ev  # chemical pot (eV)
# Carrier Concentration in cm^{-3} in 3 column
trace[:, 2] *= (1 / vol)  # cm^-3
# Changing Seebeck to microV/K
# trace[:,4] *= 1e+6            #microV/K  # it creates problem in Power factor
# print(trace.shape)
# trace[:,5] *= 1e-19
# trace[:,7] *= 1e-14


newarr2 = trace.reshape((1, trace.shape[0], trace.shape[1]))
fg = open('shifted-condtens', 'w')
for slice_2d in newarr2:
    np.savetxt(fg, slice_2d, fmt='%2.2e')
fg.close()

print("With chemical pot")
T = [300]
for temp in T:
    j = int(int(temp / 100) - 3)

    ff_xx = open(str(temp) + '.00.Conductivity_xx.dat', 'w')
    ff_yy = open(str(temp) + '.00.Conductivity_yy.dat', 'w')
    ff_zz = open(str(temp) + '.00.Conductivity_zz.dat', 'w')
    gg_xx = open(str(temp) + '.00.seebeck_xx.dat', 'w')
    gg_yy = open(str(temp) + '.00.seebeck_yy.dat', 'w')
    gg_zz = open(str(temp) + '.00.seebeck_zz.dat', 'w')
    hh_xx = open(str(temp) + '.00.T_Conductivity_xx.dat', 'w')
    hh_yy = open(str(temp) + '.00.T_Conductivity_yy.dat', 'w')
    hh_zz = open(str(temp) + '.00.T_Conductivity_zz.dat', 'w')
    kk_xx = open(str(temp) + '.00.pf_vs_mu_xx.dat', 'w')
    kk_yy = open(str(temp) + '.00.pf_vs_mu_yy.dat', 'w')
    kk_zz = open(str(temp) + '.00.pf_vs_mu_zz.dat', 'w')





    for i in range(0, trace.shape[0]):
        if trace[i, 1] == temp:
            ff_xx.write(str(trace[i, 0]) + ' ' + str(trace[i, 3]) + '\n')
            ff_yy.write(str(trace[i, 0]) + ' ' + str(trace[i, 7]) + '\n')
            ff_zz.write(str(trace[i, 0]) + ' ' + str(trace[i, 11]) + '\n')
            gg_xx.write(str(trace[i, 0]) + ' ' + str(trace[i, 12]) + '\n')
            gg_yy.write(str(trace[i, 0]) + ' ' + str(trace[i, 16]) + '\n')
            gg_zz.write(str(trace[i, 0]) + ' ' + str(trace[i, 20]) + '\n')
            hh_xx.write(str(trace[i, 0]) + ' ' + str(trace[i, 21]) + '\n')
            hh_yy.write(str(trace[i, 0]) + ' ' + str(trace[i, 25]) + '\n')
            hh_zz.write(str(trace[i, 0]) + ' ' + str(trace[i, 29]) + '\n')
            kk_xx.write(str(trace[i, 0]) + ' ' + str(trace[i, 12] * trace[i, 12] * trace[i,3])+'\n')
            kk_yy.write(str(trace[i, 0]) + ' ' + str(trace[i, 16] * trace[i, 16] * trace[i,7])+'\n')
            kk_zz.write(str(trace[i, 0]) + ' ' + str(trace[i, 20] * trace[i, 20] * trace[i,11])+'\n')



ff_xx.close()
ff_yy.close()
ff_zz.close()
gg_xx.close()
gg_yy.close()
gg_zz.close()
hh_xx.close()
hh_yy.close()
hh_zz.close()
print("With carrier concentration")
carriers = ['e', 'h']
for item in carriers:
    for temp in T:
        j = int(int(temp / 100) - 3)
        f = open('Ele-' + str(item) + '-' + str(temp) + '-xx.dat', 'w')
        g = open('Ele-' + str(item) + '-' + str(temp) + '-yy.dat', 'w')
        h = open('Ele-' + str(item) + '-' + str(temp) + '-zz.dat', 'w')
        for i in range(0, index):
            if trace[i, 1] == temp and item == 'h':
                f.write(str(trace[i, 2]) + ' ' + str(trace[i, 3]) + '\n')
                g.write(str(trace[i, 2]) + ' ' + str(trace[i, 7]) + '\n')
                h.write(str(trace[i, 2]) + ' ' + str(trace[i, 11]) + '\n')

        for i in range(index + 1, trace.shape[0]):
            if trace[i, 1] == temp and item == 'e':
                trace[i, 2] *= -1
                trace[i, 4] *= -1
                f.write(str(trace[i, 2]) + ' ' + str(trace[i, 3]) + '\n')
                g.write(str(trace[i, 2]) + ' ' + str(trace[i, 7]) + '\n')
                h.write(str(trace[i, 2]) + ' ' + str(trace[i, 11]) + '\n')

f.close()
g.close()
h.close()

