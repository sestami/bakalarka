from math import *
import sys
import numpy

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
histFile = file(fileName+'.histogram','w') #sobour pro vypis histogramu

# citac vynechanych radku
inData = 0

# promena pro ochovani
L_list = []
D_list = []
H_list = []
D_high_list = []
H_high_list = []

outFile.write('#;X;Y;A;B;V;k;L;D;H\n')

for str_line in inFile:
	if (inData == 2):
		# pocitame
		data = str_line[:-1].split(',')
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

		H = D * Q
		outFile.write(data[0]+';'+data[1]+';'+data[2]+';'+data[4]+';'+data[5]+';'+str(V)+';'+str(k)+';'+str(L)+';'+str(D)+';'+str(H)+'\n')
		L_list.append(L)
		D_list.append(D)
		H_list.append(H)
		

	# vynechava radky s metadaty
	if (inData == 1): 

		inData = 2
	if (str_line[0] == '<' and str_line[7]=='2'):	
		inData = 1

	if (inData == 0):		
		vstup = str_line[:-1].split(',')
		#print vstup[0]
		if (vstup[0]=='ProcArea'):
			ProcArea = float(vstup[1])/1e8


outFile.close()

Dsum = sum(D_list)
Hsum = sum(H_list)

histFile.write('D = '+str(Dsum)+'\n')
histFile.write('H = '+str(Hsum)+'\n')
histFile.write('\n')

