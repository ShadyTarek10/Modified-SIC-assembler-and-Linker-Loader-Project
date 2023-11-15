from pass_one import addr,sym , opFormat1,opFormat3,start
pass1=open("out_pass1.txt","r")
hte=open("HTE.txt","w")
pass2=open("out_pass2.txt","w")
symb=open("symbTable.txt","r")
address=addr
start="0x"+start
line1=pass1.readline()
x=line1.split()
x.append("ObjectCode")
pass2.write(" ".join(x))
pass2.write("\n")
progName=x[1]
if len(progName) < 6:
                for i in range(6-len(progName)):
                    progName = progName+"x"

progLength=hex(int(address,16)-int(start,16))
progLength=progLength.replace('0x','')
if len(progLength)<6:
    for i in range(6-len(progLength)):
        progLength="0"+progLength


st = start
if len(st) < 6:
     for i in range(6-len(st)):
        st = "0"+st
hrecord    = "H, " + progName + ", " +st+ ", " + progLength
hte.write(hrecord+"\n")

for line in pass1:
    x=line.split()
    if x[3] == "*":
        x[3]="-"
    if x[1]== "-":
        x[1]=="\t\t"
    if(x[2]=="RESW" or x[2]=="RESB"):
        x.append("no obcode")
        pass2.write(" ".join(x)+"\n")
    
    elif x[2] in opFormat1.keys():
        x.append(opFormat1[x[2]])
        pass2.write(" ".join(x)+"\n")  

    elif x[2]=="BYTE":
        if   x[3][0] == 'X':
            hexa=""
            for i in (2,len(x[3])-2):
                hexa=hexa+x[3][i]  
            if len(hexa)==1:
                hexa="0"+hexa 
            x.append(hexa)
            pass2.write(" ".join(x)+"\n")         
        elif x[3][0] == 'C':
            asci=""
            for i in range(2,len(x[3])-1):
                asci=asci+str(hex(ord(x[3][i])))
            x.append(asci.replace('0x',''))
            pass2.write(" ".join(x)+"\n") 

    elif x[2]=="WORD":
        wrd=""
        wrd=wrd+str(hex(int(x[3])))
        wrd=wrd.replace('0x','')
        if len(wrd)<6:
            for i in range(6-len(wrd)):
                wrd="0"+wrd
        x.append(wrd)
        pass2.write(" ".join(x)+"\n")
    elif x[2] in opFormat3.keys():
        if x[2]=="RSUB":
            opcode=opFormat3[x[2]]+"0000"
            x.append(opcode)
            pass2.write(" ".join(x)+"\n") 
        elif x[3] in sym.keys():
            norm=sym[x[3]]
            norm=norm.replace('0x','')
            obcode=opFormat3[x[2]]+norm
            x.append(obcode)
            pass2.write(" ".join(x)+"\n") 
        elif x[3][0] == "#":
            opcode = hex(int(opFormat3[x[2]],16)+1)
            opcode = opcode.replace('0x','')
            addr = x[3][1:]
            addr = hex(int(addr))
            addr = addr.replace('0x','')
            if len(opcode) < 2:
                 for i in range(2-len(addr)):
                    addr = "0"+addr
            if len(addr) < 4:
                 for i in range(4-len(addr)):
                    addr = "0"+addr
            opcode = opcode + addr
            x.append(opcode)
            pass2.write(" ".join(x)+"\n")
        elif x[3][len(x[3])-2]==",":
            label=x[3][0:len(x[3])-2]
            location=sym[label]
            location = location.replace('0x','')
            add=str(8000)
            addr = hex((int(add,16))+int(location,16))
            addr = addr.replace('0x','')
            opcode=opFormat3[x[2]]
            objectcode=opcode+addr
            x.append(objectcode)
            pass2.write(" ".join(x)+"\n")



pass2.close()
pass2=open("out_pass2.txt","r")

line_1=pass2.readline()

tstart   = 0
tlimit   = 0
n        = 0
flag     = 1
flagos   = 0 
flagEndT = 0
flagnos  = 0
str1    = ""
str2     = ""
flagTen  = 0
for i in pass2.readlines():
    x = i.split()
    n+=1
    str2    =''
    flagTen = 0
    if flagEndT == 1:
        tstart = int(x[0],16)
        flagEndT = 0
    if start == x[0]:
        hte.write("T")
        tstart = int(start,16)
        hm = str(hex(tstart)).replace('0x','')
        if len(hm) < 6:
                for i in range(6-len(hm)):
                    hm = "0"+hm
        hte.write(", " + hm)

    if x[2] =="RESB" or x[2]=="RESW":
        tstart = int(x[0],16)
        mod   = str(hex(tlimit+3))
        if len(mod) < 4:
                for i in range(4-len(mod)):
                    mod = "0"+mod
        str2 = ", "+mod
        str2 = str2.replace('0x','')
        str2 = str2 + str1
        if len(str2) >=6:
            hte.write(str2)
        tlimit = 0
        flagos = 0
        flagEndT = 1
        str2 = ''
        str1= ''
        continue
    if tlimit >= 27:
        tstart = int(x[0],16)
        mod = str(hex(tlimit+3))
        if len(mod) < 4:
                for i in range(4-len(mod)):
                    mod = "0"+mod
        str2 = ", "+mod
        str2 = str2.replace('0x','')
        str2 = str2 + str1
        hte.write(str2)
        str2 = ''
        str1= ''
        tlimit = 0
        flagos = 0 
        flagTen = 1
    
    if tlimit < 27:
        if tlimit == 0  and n > 2 and flagos == 0 :
            hte.write("\nT")
            hm = str(hex(tstart)).replace('0x','')
            if len(hm) < 6:
                for i in range(6-len(hm)):
                    hm = "0"+hm
            hte.write(", " + hm)
            flagos = 1

        mod = str(hex(tlimit+3))
        if len(mod) < 4:
                for i in range(4-len(mod)):
                    mod = "0"+mod
        str2 = ", "+mod
        str2 = str2.replace('0x','')

        str1+= str(", "+str(x[4]))
        tlimit = int(x[0],16) - tstart
if flagTen != 1:
    hte.write(str2+str1)



erecord    = "E, "+st
hte.write("\n"+erecord+"\n")

pass1.close()
hte.close()
pass2.close()
symb.close()