osaX=[]
with open('LETintervaly.txt', 'r') as f:
    for line in f:
        osaX.append(float(line.strip('\n')))

print type(osaX[0])
print osaX[0]
