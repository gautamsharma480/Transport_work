import numpy as np
#import matplotlib.pyplot as plt
#import pandas as pd
import sys
#prefix = sys.argv[1]
ry2ev=13.605698066
bohr2angs=0.529177249
ev2ry=1/ry2ev

prefix = "" # Enter the name of the prefix of trace file.
trace = np.loadtxt(prefix+'.trace')
kl=np.loadtxt('kappa.txt') # Provide Lattice thermal conductivity as a function of temperature in steps of 100.

print("Enter 1 if you want plot with Chemical potential")
with_cp = int(input()) # Enter 1 for plots with chemical potential else you will get plots with carrier concentration.

#for i in range(0,4):
#    print(kl[i,0],kl[i][1])

f = open('nscf.out', 'r')
f_pw = f.readlines()
f.close()
shift_gap = 0

for line in f_pw:

    if 'unit-cell' in line:
           vol = float(line.split()[3])*(bohr2angs**3)*1e-24
    if 'highest occupied, lowest unoccupied level' in line:
       if shift_gap == 0:
          VBM = float(line.split()[6])
          CBM = float(line.split()[7])
          Fermi = (VBM+CBM)*0.5
          #print('Fermi=', Fermi,'eV' ) 
    if 'Fermi' in line:
          Fermi = float(line.split()[4])
print('Fermi=', Fermi,'eV' )
   

#print(trace.shape)

def  prn(x,n):   ## printing nn number of digits after decimal 
        if n == 3:
            xx = '%1.2e' % x
        else:
            xx = '%.5f' % x
        return xx


def closest(lst, K):
     lst = np.asarray(lst) 
     idx = (np.abs(lst - K)).argmin() 
     return idx 

cp = []  # cp => to store chemical potential 
for i in range(0,trace.shape[0]):
        cp.append(trace[i,0])

index = closest(cp,Fermi*ev2ry)          # checking where Ef-cp = 0 and find index of row
print('index',index)
print("Fermi=",trace[index,0],", Nf=",trace[index,2])

"Fermi is subtracted : "
trace[:,0] -= trace[index,0]  # E-Ef # its in Ry here

#trace[:,2] -= trace[index,2]  # N-Nf
print('Nf not subtracted')

trace[:,0] *= ry2ev           # chemical pot (eV) 
# Carrier Concentration in cm^{-3} in 3 column
trace[:,2] *= (1/vol)         # cm^-3
# Changing Seebeck to microV/K
#trace[:,4] *= 1e+6            #microV/K  # it creates problem in Power factor
#print(trace.shape)
#trace[:,5] *= 1e-19  
#trace[:,7] *= 1e-14


newarr2 = trace.reshape((1,trace.shape[0], trace.shape[1]))
fg = open('shifted-trace', 'w')
for slice_2d in newarr2:
        np.savetxt(fg, slice_2d,fmt='%2.2e')
fg.close()

#T = [300,400,500]
if with_cp==1:
	print("With chemical pot")
	T = [300,400,500] # Temperatures you are interested in.
	for temp in T:
		j=int(int(temp/100)-3)
		ff=open(str(temp)+'.00.seebeck.dat','w')
		gg=open(str(temp)+'.00.Conductivity.dat','w')
		hh=open(str(temp)+'.00.T_Conductivity.dat','w')
		iii=open(str(temp)+'.00.pf_vs_mu.dat','w')
		jjj=open(str(temp)+'.00.ZT.dat','w')
		for i in range(0,trace.shape[0]):
			if trace[i,1] == temp:
				ff.write(str(trace[i,0]) +' '  + str(trace[i,4])+'\n') # S
				gg.write(str(trace[i,0]) +' '  + str(trace[i,5])+'\n') # Sigma 
				hh.write(str(trace[i,0]) +' '  + str(trace[i,7])+'\n') # Ke
				iii.write(str(trace[i,0]) +' '  + str(trace[i,5]*trace[i,4]**2)+'\n') # PF
				jjj.write(str(trace[i,0]) +' '+str(trace[i,5]*float(temp)*(trace[i,4]**2)/(trace[i,7] + kl[j,1]))+'\n')   # ZT


	ff.close()
	gg.close()
	hh.close()
	iii.close()
	jjj.close()
else:
	T = [300,400,500]  # Temperatures you are interested in.
	print("With carrier concentration")
	carriers=['e','h']       
	for item in carriers:
		for temp in T:
			j=int(int(temp/100)-3)
			f=open('seebeck-'+str(item)+'-'+str(temp)+'.dat','w')
			g=open('Ele-'+str(item)+'-'+str(temp)+'.dat','w')
			h=open('Th-'+str(item)+'-'+str(temp)+'.dat','w') 
			ii=open('PF-'+str(item)+'-'+str(temp)+'.dat','w')
			jj=open('ZT-'+str(item)+'-'+str(temp)+'.dat','w')
			for i in range(0,index):
				if trace[i,1] == temp and item=='h':
					f.write(str(trace[i,2]) +' '+ str(trace[i,4])+'\n') # S
					g.write(str(trace[i,2]) +' '+ str(trace[i,5])+'\n') # Sigma
					h.write(str(trace[i,2]) +' '+ str(trace[i,7])+'\n') # Ke
					ii.write(str(trace[i,2]) +' '+ str(trace[i,5]*(trace[i,4]**2))+'\n') # PF
					jj.write(str(trace[i,2]) +' '+str(trace[i,5]*float(temp)*(trace[i,4]**2)/(trace[i,7]+kl[j,1]))+'\n')
			for i in range(index+1,trace.shape[0]):
				if trace[i,1] == temp and item=='e':
					trace[i,2] *= -1  # -x=>  +x
					trace[i,4] *= -1  # -S => +S
					f.write(str(trace[i,2]) +' '+ str(trace[i,4])+'\n')
					g.write(str(trace[i,2]) +' '+ str(trace[i,5])+'\n')
					h.write(str(trace[i,2]) +' '+ str(trace[i,7])+'\n') 
					ii.write(str(trace[i,2]) +' '+ str(trace[i,5]*(trace[i,4]**2))+'\n')
					jj.write(str(trace[i,2]) +' '+str(trace[i,5]*float(temp)*(trace[i,4]**2)/(trace[i,7]+kl[j,1]))+'\n')	   
	f.close()
	g.close()
	h.close()
	ii.close()
	jj.close()
