from math import *
import sys
import numpy
import matplotlib.pyplot as plt

# fileName=sys.argv[1]

# f=open(fileName+'.results','r')
# g=open(fileName+'.histogram','w')

f=open('Img.nap.results','r')
g=open('Img.nap.histogram','w')

L_list=[]

inData=0
for line in f:
    if inData==1:
        data=line[:].split(';')
        L_list.append(float(data[7]))
    if inData==0:
        inData=1

f.close()

print 'pocet stop skutecny:' + str(len(L_list))

# vyhotoveni LET spekter
g.write('#LET '+'cetnost\n')

Lmin=floor(min(L_list)/10.0)*10
# Lmax=max(L_list)
Lmax=ceil(max(L_list)/10.0)*10

print 'minimalni LET: '+str(min(L_list))
print 'maximalni LET: '+str(max(L_list))

print 'minimalni LET zaokrouhlen: '+str(Lmin)
print 'maximalni LET zaokrouhlen: '+str(Lmax)

#NASTAVUJE SE POCET INTERVALU 
# pocetBinu=100 
# sirkaIntervalu=(Lmax-Lmin)/pocetBinu

# print 'sirkaIntervalu: ' + str(sirkaIntervalu)
# print 'sirkaIntervalu/2: ' + str(sirkaIntervalu/2)
# print 'posledni x-ova hodnota ziskana z sirkyIntervalu: ' + str(Lmin+pocetBinu*sirkaIntervalu) #toto ok

#NASTAVUJE SE SIRKA INTERVALU
sirkaIntervalu=10
pocetBinu=int((Lmax-Lmin)/sirkaIntervalu)
print 'pocetBinu: ' + str(pocetBinu)
print 'posledni x-ova hodnota ziskana z sirkyIntervalu: ' + str(Lmin+pocetBinu*sirkaIntervalu) #toto ok

osaX=[]
for i in xrange(1,pocetBinu+1):
    osaX.append(Lmin+sirkaIntervalu*i)

# osaX=numpy.linspace(Lmin,Lmax,pocetBinu)
# sirkaIntervalu=(1000-1)/pocetBinu
# osaX=numpy.logspace(0,3,pocetBinu)

print 'delka pole osaX: ' + str(len(osaX)) # toto taky ok
# print 'osa x: ' + str(osaX)

pocetNezaznamenanychStop=0
# cetnost=[]
# for x in osaX:
    # citac=0
    # for LET in L_list:
        # if (LET>=(x-sirkaIntervalu/2) and LET<=(x+sirkaIntervalu/2)): #zde vznikaji chyby z duvodu nepresnosti
            # citac+=1
        # else:
            # pocetNezaznamenanychStop+=1
    # cetnost.append(citac)
    # g.write(str(x)+' '+str(citac)+'\n')

#PROCHAZENI V OPACNEM SMERU
cetnost=[0]*pocetBinu
for LET in L_list:
    i=0
    nezaznamenani=0
    for x in osaX:
        if (LET>=(x-sirkaIntervalu/2) and LET<=(x+sirkaIntervalu/2)):
            cetnost[i]+=1
            nezaznamenani=0
            break
        else:
            nezaznamenani=1
        i+=1
    if nezaznamenani==1:
        pocetNezaznamenanychStop+=1

for i in xrange(pocetBinu):
    g.write(str(osaX[i])+' '+str(cetnost[i])+'\n')


g.close()

print 'pocet stop jako suma N z osy y: '+ str(sum(cetnost))
print 'pocet stop, ktere se nezaradily do zadneho intervalu: '+ str(pocetNezaznamenanychStop)

# vykresleni
# plt.plot(osaX,cetnost)
plt.step(osaX,cetnost,where='mid')
plt.xlabel('$LET$ [keV/$\mu$m]')
plt.ylabel('$N$ [-]')
plt.xscale('log')
plt.yscale('log')
# plt.grid()
plt.show()
