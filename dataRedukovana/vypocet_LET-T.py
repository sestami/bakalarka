from math import *
import sys
import numpy
import matplotlib.pyplot as plt
# from matplotlib import rc

# rc('font', **{'family':'serif','serif':['Palatino']})
# rc('text', usetex=True)

# import matplotlib as mpl
# print mpl.__version__

ELV2J = 0.000001602

zp_pouz = "Zpusob pouziti: python vypocet_L.py jmeno_souboru hodnota_B <spodni mez stupnice> <horni mez stupnice> <pocet intervalu v histogramu> <log10> <threshold pro sumovani D a H>"

if (len(sys.argv) < 3):
	print "Malo parameteru na prikazove radce!"
	print zp_pouz
	sys.exit(1)

fileName = sys.argv[1]
B = float(sys.argv[2])

# priradi spodni meze stupnice, pokud neni zadano, pouzije 0
if (len(sys.argv) > 3):
	minX = float(sys.argv[3])
else:
	minX = 0.

# overi zadani horni meze stupni, pokud neni zadano, pouzije 200
if (len(sys.argv) > 4):
	maxX = float(sys.argv[4])
	if (minX >= maxX):
		print "Horni mez stupnice musi byt ostre vetsi nez spodni mez"
		print zp_pouz
		sys.exit(1)
else:
	maxX = 200.

# pocet intervalu v histogramu, defaultne se bere 20. Promenna N_int uchovava celkovy pocet mezi
if (len(sys.argv) > 5):
	N_int = int(sys.argv[5])+1
else:
	N_int = 21

# vytvori stupnici pro rozrazovani, defaultne bere linearni
scale = numpy.linspace(minX, maxX, N_int)
logsc = False

if (len(sys.argv) > 6):
	if (sys.argv[6] == 'log'):
		scale = numpy.logspace(log10(minX), log10(maxX), N_int)
		logsc = True

if (len(sys.argv) > 7):
	threshold = float(sys.argv[7])
else:
	threshold = 10

# otevreni souboru pro vstup a vystup
inFile = file(fileName,'r') #vstupni soubor
outFile = file(fileName+'.results','w') #soubor pro vypis vsech spoctenych hodnot
histFile = file(fileName+'.histogram','w') #soubor pro vypis histogramu
davkaFile = file(fileName+'.davky','w') # soubor pro zapsani celkovych davek a davkovych ekvivalentu, resp. jejich prikonu

# citac vynechanych radku
inData = 0

# promenna pro uchovani; 
L_list = []
D_list = []
H_list = []
V_list = []
D_high_list = []
H_high_list = []

outFile.write('#;X;Y;A;B;V;k;L;D;H\n')

for str_line in inFile:
	if (inData == 2):
		# pocitame
                data = str_line[:-1].split(',') #[:-1] slices the string to omit the last character
		V = sqrt(1+4*pow(float(data[4])/B,2)/pow(1-pow(float(data[5])/B,2),2))
		L = -99.8424+125.00172*V-15.28166*(V*V)+2.04636*(V*V*V)
		k = V*V/(V*V-1)
		D = ELV2J * L * k * 2 / ProcArea

		if (L<=10):
			Q = 1
		if ((L>10) and (L<100)):
			Q = 0.32*L-2.2
		if (L>=100):
			Q = 300 / sqrt(L)
                if (L<=1000):
		    H = D * Q
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
		#print vstup[0]
		if (vstup[0]=='ProcArea'):
			ProcArea = float(vstup[1])/1e8 #1e8==1*(10**8)


outFile.close()

# ZAPSANI DAVKY A DAVKOVEHO EKVIVALENTU
time=180 #dni

Dsum = sum(D_list)
Hsum = sum(H_list)

Drate=(Dsum*1000)/time
Hrate=(Hsum*1000)/time

davkaFile.write('D (mGy) = '+str(Dsum)+'\n')
davkaFile.write('H (mSv) = '+str(Hsum)+'\n')
davkaFile.write('Drate (uGy/day) = '+str(Drate)+'\n')
davkaFile.write('Hrate (uSv/day) = '+str(Hrate)+'\n')

davkaFile.close()

# VYHOTOVENI LET SPEKTER
print 'pocet stop skutecny: ' + str(len(L_list))

histFile.write('#LET '+'cetnost '+'davka '+'davkovyEkvivalent '+'fluece\n')

osaX=[]
with open('LETintervaly.txt', 'r') as f:
    for line in f:
        osaX.append(float(line.strip('\n')))

stredyIntervalu=[]
with open('LETstredIntervalu.txt', 'r') as f:
    for line in f:
        stredyIntervalu.append(float(line.strip('\n')))

# Lmin=floor(min(L_list)/10.0)*10
# # Lmax=max(L_list)
# Lmax=ceil(max(L_list)/10.0)*10

print 'minimalni LET: '+str(min(L_list))
print 'maximalni LET: '+str(max(L_list))

# print 'minimalni LET zaokrouhlen: '+str(Lmin)
# print 'maximalni LET zaokrouhlen: '+str(Lmax)

#NASTAVUJE SE POCET INTERVALU 
# pocetBinu=100 
# sirkaIntervalu=(Lmax-Lmin)/pocetBinu

# print 'sirkaIntervalu: ' + str(sirkaIntervalu)
# print 'sirkaIntervalu/2: ' + str(sirkaIntervalu/2)
# print 'posledni x-ova hodnota ziskana z sirkyIntervalu: ' + str(Lmin+pocetBinu*sirkaIntervalu) #toto ok

#NASTAVUJE SE SIRKA INTERVALU
# sirkaIntervalu=10
# pocetBinu=int((Lmax-Lmin)/sirkaIntervalu)
# print 'pocetBinu: ' + str(pocetBinu)
# print 'posledni x-ova hodnota ziskana z sirkyIntervalu: ' + str(Lmin+pocetBinu*sirkaIntervalu) #toto ok

# osaX=[]
# for i in xrange(1,pocetBinu+1):
    # osaX.append(Lmin+sirkaIntervalu*i)

# osaX=numpy.linspace(Lmin,Lmax,pocetBinu)
# sirkaIntervalu=(1000-1)/pocetBinu
# osaX=numpy.logspace(0,3,pocetBinu)

# print 'delka pole osaX: ' + str(len(osaX)) # toto taky ok
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
    # histFile.write(str(x)+' '+str(citac)+'\n')

#PROCHAZENI V OPACNEM SMERU
cetnost=[0]*len(stredyIntervalu)
davka=[0]*len(stredyIntervalu)
ekvDavka=[0]*len(stredyIntervalu)

#informace pro fluenceSpektrum
Vsum=[0]*len(stredyIntervalu)

for i in xrange(len(L_list)):
    # k=0 # k-ty bin
    nezaznamenani=0
    for j in xrange(1,len(osaX)+1):
        if (L_list[i]>=osaX[j-1] and L_list[i]<=osaX[j]):
            cetnost[j-1]+=1
            davka[j-1]+=D_list[i]*1000
            ekvDavka[j-1]+=H_list[i]*1000
            Vsum[j-1]+=V_list[i]

            nezaznamenani=0
            break
        else:
            nezaznamenani=1
        # k+=1
    if nezaznamenani==1:
        pocetNezaznamenanychStop+=1


Vprumer=[0]*len(stredyIntervalu)
cosTheta=[0]*len(stredyIntervalu)
fluence=[0]*len(stredyIntervalu)
for i in xrange(len(cetnost)):
    Vprumer[i]=Vsum[i]/cetnost[i]
    cosTheta[i]=(Vprumer[i]**2-1)/Vprumer[i]**2
    fluence[i]=cetnost[i]/(2*pi*cosTheta[i]*ProcArea) #ProcArea asi v um^2

for i in xrange(len(stredyIntervalu)):
    histFile.write(str(stredyIntervalu[i])+' '+str(cetnost[i])+' '+str(davka[i])+' '+str(ekvDavka[i])+' '+str(fluence[i])+'\n')


histFile.close()

print 'pocet stop jako suma N z osy y: '+ str(sum(cetnost))
print 'pocet stop, ktere se nezaradily do zadneho intervalu: '+ str(pocetNezaznamenanychStop)

print '\ncelkova davka originalne: '+ str(Dsum)
print 'celkova davka ze spektra: '+ str(sum(davka)/1000)

print '\ncelkovy davkovy ekvivalent originalne: '+ str(Hsum)
print 'celkovy davokovy ekvivalent ze spektra: '+ str(sum(ekvDavka)/1000)
# vykresleni
# plt.plot(osaX,cetnost)
# plt.step(stredyIntervalu,cetnost,where='mid')
# plt.xlabel('$LET$ [keV/$\mu$m]',fontsize=15)
# plt.ylabel('$N$ [-]',fontsize=15)
# plt.title('PDP 1',fontsize=25)
# plt.xscale('log')
# plt.yscale('log')
# # plt.grid()
# # plt.show()
# plt.savefig('praktickaCast_spektrum1.eps',bbox_inches='tight')

