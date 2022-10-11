import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
data=open('hetero.trace', "r")
data.readline()
a=data.readlines()
ry_ev=13.605698066
ef=14.0595
cc_ef=0.0000000
vol=53.28841810126380976678*1e-24  # cm-3
#print(len(a))
htmp=float(input('give me highest temperature used in ur calculation'))
rng=float(input('delta T ?'))
times=htmp/rng-1
itr1=0
while itr1 <=times:
      bb=300.000#rng*itr1+rng
      cb=open(f'seebeck_{bb}k.dat', 'w')
      elc=open(f'el_conductivity_{bb}k.dat', 'w')
      eth=open(f'thermal_cond_{bb}k.dat', 'w')
      pf=open(f'power_factor_{bb}k.dat', 'w')
      zt=open(f'zt_{bb}k.dat', 'w')
      dos=open(f'dos_{bb}k.dat', 'w')
      cc=open(f'cc_{bb}k.dat', 'w')
      for x in a:
          aa=x.split()
          if float(aa[1])==bb:
             first=str(float(aa[0])*ry_ev-ef)
             car_cm=str((float(aa[2])-cc_ef)/vol)
             pff=str(float(aa[4])*float(aa[4])*float(aa[5]))
#             ztt=str(float(aa[4])*float(aa[4])*float(aa[5])*bb/float(aa[7]))
             cb.write(first  + "\t"  + aa[4]  + "\t"  + car_cm +  "\n") 
             elc.write(first + "\t"  + aa[5]  + "\t"  + car_cm +  "\n")
             eth.write(first + "\t"  + aa[7]  + "\t"  + car_cm + "\n")
             pf.write(first  + "\t"  + pff    + "\t"  + car_cm + "\n")
#             zt.write(first + "\t" + ztt +  "\n")
             dos.write(first + "\t" + aa[3] + "\n" )
             cc.write(first + "\t"  + car_cm + "\n")
      itr1+=1

# plotting the combind plot of seebeck coefficient
def cbplot(bb):
    itr1=0
    while itr1<=times:
         bb=rng*itr1+rng
         rcb=np.loadtxt(f'seebeck_{bb}k.dat')
         plt.plot(rcb[:,0], rcb[:,1]*1e6, label=f'{bb}K')
         plt.legend()
         itr1+=1
         plt.savefig('cb_all_tmpK.eps', dpi=500)
         plt.xlabel('\u03bc(eV)')
         plt.ylabel('S(\u03bcV/K)')
         plt.xlim(-3,1)
         plt.yticks(np.arange(-3000,3000,500))

# plotting the combined plot of electrical conductivity
def elcplot(bb):
    itr1=0
    while itr1<=times:
          bb=rng*itr1+rng
          relc=np.loadtxt(f'el_conductivity_{bb}k.dat')
          plt.plot(relc[:,0], relc[:,1], label=f'{bb}K')
          plt.legend()
          itr1+=1
          plt.savefig('elc_all_tmpK.eps', dpi=500)
          plt.xlabel('\u03bc(eV)')
          plt.ylabel('\u03c3/\u03c4(S/m sec)')
          plt.xlim(-3,1)
          plt.ylim(0,0.5e21,0.5e20)

# plotting the combined plot of electronic thermal conductivity
def ethplot(bb):
    itr1=0
    while itr1<=times:
          bb=rng*itr1+rng
          reth=np.loadtxt(f'thermal_cond_{bb}k.dat')
          plt.plot(reth[:,0], reth[:,1], label=f'{bb}K')
          plt.legend()
          itr1+=1
          plt.savefig('eth_all_tmpK.eps', dpi=500)
          plt.xlabel('\u03bc(eV)')
          plt.ylabel('\u03BA_\u03B5/\u03c4(W/m K sec)')
          plt.xlim(-3,1)
          plt.ylim(0,1e16,0.2e15)

# plotting the combined plot of power factor
def pfplot(bb):
    itr1=0
    while itr1<=times:
          bb=rng*itr1+rng
          rpf=np.loadtxt(f'power_factor_{bb}k.dat')
          plt.plot(rpf[:,0], rpf[:,1], label=f'{bb}K')
          plt.legend()
          itr1+=1
          plt.savefig('pf_all_tmpK.eps', dpi=500)
          plt.xlabel('\u03bc(eV)')
          plt.ylabel('PF(W/m K^2 sec)')
          plt.xlim(-3,1)
# plotting the combined plot of power factor
def ztplot(bb):
    itr1=0
    while itr1<=times:
          bb=rng*itr1+rng
          rzt=np.loadtxt(f'zt_{bb}k.dat')
          plt.plot(rzt[:,0], rzt[:,1], label=f'{bb}K')
          plt.legend()
          itr1+=1
          plt.savefig('zt_all_tmpK.eps', dpi=500)
          plt.xlabel('\u03bc(eV)')
          plt.ylabel('ZT')
          plt.xlim(-3,1)



cbplot(bb)
plt.close()
elcplot(bb)
plt.close()
ethplot(bb)
plt.close()
pfplot(bb)
plt.close()
#ztplot(bb)
#plt.close()
