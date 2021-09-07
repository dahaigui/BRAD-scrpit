import sys
if len(sys.argv) !=3 or "--help" in sys.argv:
	print("Usage: python counts2_TPM.py featurecounts.results Tpm.results")
	exit()
file=open(sys.argv[1],"r")
line =file.readlines()
out=open(sys.argv[2],"w")
list=[]
for i in line[2:]:
	l=i.strip().split("\t")
	num=l[-1]
	len=l[-2]
	N=int(num)/int(len)
	list.append(N)
for i in line[2:]:
	l=i.strip().split("\t")
	id=l[0]
	num=l[-1]
	len=l[-2]
	tpm=((int(num)/int(len))*(10**6))/sum(list)
	out.write(id+"\t"+str(tpm)+"\n")
file.close()
out.close()
