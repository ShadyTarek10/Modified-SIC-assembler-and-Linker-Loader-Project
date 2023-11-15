#,x without space
#lines without labels have to start with a -
#lines without addresses add * to the end
# immediate.write(x[0]+" "+x[2]+" "+x[3]+"\n")
# AT end put . instead of end

#Opening SIC program
inp = open("input.txt","r")
#For output of PASS ONE
out = open("intermediate.txt","w")
#SYMBOLTAB
symtab = open("SymbolTab.txt","w")

for line in inp.readlines():
    x=line.split()

    if x.__len__()==0:
        continue
    if x[1]==".":
        continue
    if x[1]=="END" or x[1]=="end":
        break

    out.write(x[1]+" "+x[2]+" "+x[3]+"\n")

out.write("END")
inp.close()
out.close()