import numpy as np 


def zt_cals(T,data_size):
    
    zt_p = []
    zt_n = []
    for i in range(0,data_size):
        if zt[i,0] < 0:
            zt_p.append(zt[i,1])
        else:
            zt_n.append(zt[i,1])


    ZT_p = np.array(zt_p)
    ZT_n = np.array(zt_n)

    #print("ZT_p=", np.max(ZT_p),"ZT_n=", np.max(ZT_n))
    return str(T)+"  "+str(np.max(ZT_p))+" "+str(np.max(ZT_n))
    
    
    
T=np.arange(300,1300,200)
f=open("ZT-vs-T.dat","w")
for i in T:
    print(i)
    zt = np.loadtxt(str(i)+'-ZT.dat')
    out = zt_cals(i,zt.shape[0])
    
    f.write(out+"\n")
