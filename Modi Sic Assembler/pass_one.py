inp = open("intermediate.txt","r")
pass1= open("out_pass1.txt","w")
symb= open("symbTable.txt","w")
sym={}
opFormat3 = {
	"ADD":"18",
	"AND":"40",
	"COMP":"28",
	"DIV":"24",
	"J":"3C",
	"JEQ":"30",
	"JGT":"34",
	"JLT":"38",
	"JSUB":"48",
	"LDA":"00",
	"LDCH":"50",
	"LDL":"08",
	"LDX":"04",
	"MUL":"20",
	"OR":"44",
	"RD":"D8",
	"RSUB":"4C",
	"STA":"0C",
	"STCH":"54",
	"STL":"14",
	"STSW":"E8",
	"STX":"10",
	"SUB":"1C",
	"TD":"E0",
	"TIX":"2C",
	"WD":"DC"}

opFormat1 ={
    "FIX": "C4",
    "FLOAT":"C0",
    "HIO":"F4",
    "NORM":"C8",
    "SIO": "F0",
    "TIO":"F8"
}
firstl = inp.readline()
pass1.write("Address ")
pass1.write("".join(firstl))
newl = firstl.split()
start = newl[2]
addr = newl[2]

for line in inp.readlines():
		x = line.split()
		if x[0]=="end" or x[0]=="END":
			break
		pass1.write(hex(int(addr,16))+"\t")
		pass1.write("".join(line))
		if x[0]!="-":
			symb.write(x[0]+"\t"+hex(int(addr,16))+"\n")
			sym[x[0]] = str(hex(int(addr,16)))
		if x[1] in opFormat3.keys() or x[1]=="WORD":
			addr = str(hex(int(addr,16)+(3)))
		elif x[1] in opFormat1.keys():
			addr = str(hex(int(addr,16)+(1)))
		elif x[1]=="RESW":
			temp = int(x[2],16)
			addr = str(hex(int(addr,16)+(temp)*3))
		elif x[1]=="RESB":
			addr = str(hex(int(addr,16)+int(x[2])))
		elif x[1]=="BYTE":
			if x[2][0]=="X":
				addr = str(hex(int(addr,16)+int((len(x[2])-3)/2)))
			elif x[2][0]=="C":
				addr = str(hex(int(addr,16)+(len(x[2])-3)))

pass1.close()
symb.close()
inp.close()