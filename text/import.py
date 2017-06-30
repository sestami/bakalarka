from math import *
import sys
import numpy

ELV2J = 0.000001602

zp_pouz = "Zpusob pouziti: python vypocet_L.py jmeno_souboru hodnota_B "

if (len(sys.argv) < 3):
    print "Malo parameteru na prikazove radce!"
    print zp_pouz
    sys.exit(1)

fileName = sys.argv[1]
B = float(sys.argv[2])

# otevreni souboru pro vstup a vystup
inFile = file(fileName,'r') #vstupni soubor
outFile = file(fileName+'.results','w') #soubor pro vypis vsech spoctenych hodnot
histFile = file(fileName+'.histogram','w') #soubor pro vypis hodnot do histogramu
davkaFile = file(fileName+'.davky','w') # soubor pro zapsani celkovych davek a davkovych ekvivalentu

# citac vynechanych radku
inData = 0

# promenne pro uchovani 
L_list = []
D_list = []
H_list = []
V_list = []

outFile.write('#;X;Y;A;B;V;k;L;D;H\n')

for str_line in inFile:
    if (inData == 2):
        data = str_line[:-1].split(',')
        V = sqrt(1+4*pow(float(data[4])/B,2)/pow(1-pow(float(data[5])/B,2),2))
        L = -99.8424+125.00172*V-15.28166*(V*V)+2.04636*(V*V*V)
        k = V*V/(V*V-1)
        D = ELV2J * L * k * 2 / ProcArea # v mGy
        if (L<=10):
            Q = 1
        elif ((L>10) and (L<100)):
            Q = 0.32*L-2.2
        elif (L>=100):
            Q = 300 / sqrt(L)

        if (L<=1000): # kvuli rozsahu kalibracni krivky
            H = D * Q # v mSv
            outFile.write(data[0]+';'+data[1]+';'+data[2]+';'+data[4]+';'+data[5]+';'+str(V)+';'+str(k)+';'+str(L)+';'+str(D)+';'+str(H)+'\n')
            L_list.append(L)
            D_list.append(D)
            H_list.append(H)
            V_list.append(V)

    # vynechava radky s metadaty
    if (inData == 1): 
        inData = 2
    if (str_line[0] == '<' and str_line[7]=='2'):	
        inData = 1
    if (inData == 0):		
        vstup = str_line[:-1].split(',')
        if (vstup[0]=='ProcArea'):
            ProcArea = float(vstup[1])/1e8 
outFile.close()

# zapsani davky a davkoveho ekvivalentu
time=180 #dni

Dsum = sum(D_list)
Hsum = sum(H_list)

Drate=(Dsum*1000)/time
Hrate=(Hsum*1000)/time

davkaFile.write('D [mGy] = '+str(Dsum)+'\n')
davkaFile.write('H [mSv] = '+str(Hsum)+'\n')
davkaFile.write('Drate [uGy/day] = '+str(Drate)+'\n')
davkaFile.write('Hrate [uSv/day] = '+str(Hrate)+'\n')

davkaFile.close()

# vyhotoveni dat na LET spektra
print 'pocet stop: ' + str(len(L_list))

histFile.write('#LET '+'cetnost '+'davka[uGy] '+'davkovyEkvivalent[mSv] '+'fluence[cm^-2 sr^-1]\n')

# externi soubory obsahuji LET intervaly ekvidistantni na log skale
intervaly=[]
with open('LETintervaly.txt', 'r') as f:
    for line in f:
        intervaly.append(float(line.strip('\n')))

stredyIntervalu=[]
with open('LETstredyIntervalu.txt', 'r') as f: 
    for line in f:
        stredyIntervalu.append(float(line.strip('\n')))

print 'minimalni LET: '+str(min(L_list))
print 'maximalni LET: '+str(max(L_list))

pocetNezaznamenanychStop=0
cetnost=[0]*len(stredyIntervalu)
davka=[0]*len(stredyIntervalu)
davkEkv=[0]*len(stredyIntervalu)
Vsum=[0]*len(stredyIntervalu) # pro vypocet dif. fluence
for i in xrange(len(L_list)):
    nezaznamenani=0 # kontrolni promenna (zdali se roztridily vsechny stopy)
    for j in xrange(1,len(intervaly)+1):
        if (L_list[i]>=intervaly[j-1] and L_list[i]<=intervaly[j]):
            cetnost[j-1]+=1
            davka[j-1]+=D_list[i]*1000
            davkEkv[j-1]+=H_list[i]
            Vsum[j-1]+=V_list[i]
            nezaznamenani=0
            break
        else:
            nezaznamenani=1
    if nezaznamenani==1:
        pocetNezaznamenanychStop+=1

Vprumer=0
cosTheta=0
fluence=[0]*len(stredyIntervalu)
for i in xrange(len(cetnost)):
    Vprumer=Vsum[i]/cetnost[i]
    cosTheta=(Vprumer**2-1)/Vprumer**2
    fluence[i]=cetnost[i]/(2*pi*cosTheta*ProcArea) #ProcArea je analyzovana plocha v cm^2

for i in xrange(len(stredyIntervalu)):
    histFile.write(str(stredyIntervalu[i])+' '+str(cetnost[i])+' '+str(davka[i])+' '+str(davkEkv[i])+' '+str(fluence[i])+'\n')

histFile.close()

print '\npocet nezarazenych stop: '+str(pocetNezaznamenanychStop)

print '\ncelkova davka [mGy]: '+ str(Dsum)
print 'celkovy davkovy ekvivalent [mSv]: '+ str(Hsum)
print 'analyzovana plocha [cm^2]: '+ str(ProcArea)
