import re
import pandas as pd
from pandasgui import show
import itertools

num_of_progs = int(input("Please Enter Number of Programs:"))
print("Please Enter The Sequence of Programs:")
Seq_of_progs = []
Trecords     = []
ESTAB_values={}
address_code={}
headerList=[hex(int('0',16)),hex(int('1',16)),hex(int('2',16)),hex(int('3',16)),hex(int('4',16)),hex(int('5',16)),hex(int('6',16)),hex(int('7',16)),hex(int('8',16)),hex(int('9',16)),hex(int('A',16)),hex(int('B',16)),hex(int('C',16)),hex(int('D',16)),hex(int('E',16)),hex(int('F',16))]
current_length = str(0)
current_iteration = 0
for n in range(0,num_of_progs):
    Seq_of_progs.append(int(input()))
print(Seq_of_progs)

ESTAB= open("ESTAB.txt","w")
main_file = open("input.txt" , "r")
file_name = 1
for line in main_file.readlines():
    whole_line = line.split()
    if (whole_line[0] == "H"):
        if(f"{str(file_name)}.txt"):
            f = open(f"{str(file_name)}.txt","w")
        else:
            f = open(f"{str(file_name)}.txt","x")

    f.write(line)
    
    if (whole_line[0] == "E"):
        if ( file_name == num_of_progs):
            f.write("\n")
        f.close()
        file_name += 1
estab_file = open("estabgen.txt","w")
for i in range(0,num_of_progs):
    current_prog = open(f"{str(Seq_of_progs[i])}.txt","r")
    estab_file.writelines(current_prog)
    
estab_file.close()
Relocation = input("please enter the starting value in hex:")
estab_file = open("estabgen.txt","r")
for line in estab_file.readlines():
    whole_line = line.split()
    if (whole_line[0] == "H"):
        name=whole_line[1]
        # if len(name) < 6:
        #             for i in range(6-len(name)):
        #                 name =  name+"x"
        startaddr=whole_line[2]
        if current_iteration == 0:
            startaddr=whole_line[2]
            startaddr=hex((int(startaddr,16))+int(Relocation,16))
            startaddr = startaddr.replace('0x','')
            if len(startaddr) < 6:
                    for i in range(6-len(startaddr)):
                        startaddr = "0"+startaddr
        length=whole_line[3]
        if current_iteration != 0:
            startaddr = hex((int(startaddr,16))+int(current_length,16))
            startaddr = startaddr.replace('0x','')
            if len(startaddr) < 6:
                    for i in range(6-len(startaddr)):
                        startaddr = "0"+startaddr
        ESTAB.write(name+" "+"******"+" "+startaddr+" "+length+"\n")
    if whole_line[0]=="D":

        f_dname_ready = 0
        f_daddr_ready = 0
        for i in range(len(whole_line)):
            if (i % 2 == 1):
                Dname=whole_line[i]
                f_dname_ready = 1
            if (i % 2 == 0 and i!= 0):
                Daddr=whole_line[i]
                Daddr = hex((int(Daddr,16))+int(startaddr,16))
                Daddr = Daddr.replace('0x','')
                f_daddr_ready = 1
            if(f_daddr_ready and f_dname_ready):
                if len(Daddr) < 6:
                    for i in range(6-len(Daddr)):
                        Daddr = "0"+Daddr
                # if len(Dname) < 6:
                #     for i in range(6-len(Dname)):
                #         Dname =  Dname+"x"
                ESTAB.write("******"+" "+Dname+" "+Daddr+" "+"******"+"\n")
                f_daddr_ready = 0
                f_dname_ready = 0
                ESTAB_values[Dname]= Daddr
    if (whole_line[0] == "E"):
        current_length = hex((int(length,16))+int(startaddr,16))
        current_length = current_length.replace('0x','')

    current_iteration+=1

ESTAB.close()
get_new_adr = open("ESTAB.txt" , "r")
address_location= []

for line in get_new_adr.readlines():
    w = line.split(" ")
    if (w[0] != "******"):
        address_location.append(w[2])
get_new_adr.close()
get_new_adr = open("ESTAB.txt" , "r")
ad_loc ={}
for line in get_new_adr.readlines():
    w = line.split(" ")
    if (w[0] != "******"):
        ad_loc[w[0]] = w[2]       

estab_file.close()
gui_used = []
estab_file = open("estabgen.txt","r")
counter = 0
for line in estab_file.readlines():
    whole_line = line.split()
    if (whole_line[0] == "H" and counter < num_of_progs):
        current_offset= address_location[counter]
        counter+=1
    if whole_line[0] == "T":
        whole_line[1] = hex((int(whole_line[1],16))+int(current_offset,16))
        check_len     = hex((int(whole_line[1],16))+int(whole_line[2],16))
        addr_diff     = whole_line[1]
        Tstart        = addr_diff
       
        addr_diff = hex(int(addr_diff,16) & int("FFFFF0",16))
        check_len = hex(int(check_len,16) & int("FFFFF0",16))
        addr_tobe_added = hex((int(check_len,16))-int(addr_diff,16))
        third_place=int(str(addr_tobe_added)[2])

        if (Tstart not in address_code.keys()):
            gui_used.append(addr_diff)
            for i in range(0,16):
                address_code[hex((int(addr_diff,16))+i)] = "-"

        if third_place == 1:
            addr_diff = hex(int(addr_diff,16) + int(str(10),16))
            gui_used.append(addr_diff)

            for i in range(0,16):
                address_code[ hex((int(addr_diff,16))+i)] = "-"
        if third_place == 2:
            addr_diff = hex(int(addr_diff,16) + int(str(20),16))
            gui_used.append(addr_diff)

            for i in range(0,16):
                address_code[ hex((int(addr_diff,16))+i)] = "-"

        jump=0
        for x in range(3,len(whole_line)):
            for n in range(0,len(whole_line[x]),2):
                Tstart=hex((int(Tstart,16))+jump)
                address_code[Tstart]=whole_line[x][n] + whole_line[x][n+1]
                jump=1


estab_file.close()
modified_file = open("estabgen.txt","r")
counter = 0
for line in modified_file.readlines():
    whole_line = line.split()
    if (whole_line[0] == "H" and counter < num_of_progs):
        current_offset= address_location[counter]
        counter+=1
    if whole_line[0] == "M":
        whole_line[1] = hex((int(whole_line[1],16))+int(current_offset,16))

        symbol        = whole_line[3][1:] 
        if (symbol in ESTAB_values.keys()):
          addr_concat = ESTAB_values[symbol]
        
        if symbol in ad_loc.keys():
            addr_concat = ad_loc[symbol]

        # print(addr_concat)
        x = str(hex(int(whole_line[1],16) + int(str(1),16)))
        y = str(hex(int(whole_line[1],16) + int(str(2),16)))
        
      
        second_addr = address_code[x]
        third_addr  = address_code[y]
        #print(address_code[whole_line[1]][1]+second_addr+third_addr)
        if whole_line[3][0] == "+":
            modi_whole = int(whole_line[1],16)
            if whole_line[2] == "05":
                modified_addr = address_code[whole_line[1]][1]+second_addr+third_addr
                modified_addr = hex((int(modified_addr,16))+int(addr_concat,16))
                modified_addr = modified_addr.replace('0x','')
                if len(modified_addr) < 5:
                    for i in range(5-len(modified_addr)):
                        modified_addr = "0"+modified_addr
                address_code[whole_line[1]] = address_code[whole_line[1]][0] + modified_addr[0]
                address_code[x]                = modified_addr[1] + modified_addr[2]
                address_code[y]                = modified_addr[3] + modified_addr[4]
            if whole_line[2] == "06":
                modified_addr = address_code[whole_line[1]]+second_addr+third_addr
                modified_addr = hex((int(modified_addr,16))+int(addr_concat,16))
                modified_addr = modified_addr.replace('0x','')
                if len(modified_addr) < 6:
                    for i in range(6-len(modified_addr)):
                        modified_addr = "0"+modified_addr
                address_code[whole_line[1]]    = modified_addr[0] + modified_addr[1]
                address_code[x]                = modified_addr[2] + modified_addr[3]
                address_code[y]                = modified_addr[4] + modified_addr[5]
           


        if whole_line[3][0] == "-":
            modi_whole = int(whole_line[1],16)
            if whole_line[2] == "05":
                modified_addr = address_code[whole_line[1]][1]+second_addr+third_addr
                modified_addr = hex((int(modified_addr,16))-int(addr_concat[1:],16))
                modified_addr = modified_addr.replace('0x','')
                if len(modified_addr) < 5:
                    for i in range(5-len(modified_addr)):
                        if modified_addr[0] == "f" or modified_addr[0] == "F":
                            modified_addr = "f"+modified_addr
                        else:
                            modified_addr = "0"+modified_addr
                address_code[whole_line[1]] = address_code[whole_line[1]][0] + modified_addr[0]
                address_code[x]                = modified_addr[1] + modified_addr[2]
                address_code[y]                = modified_addr[3] + modified_addr[4]
            if whole_line[2] == "06":
                modified_addr = address_code[whole_line[1]]+second_addr+third_addr
                modified_addr = hex((int(modified_addr,16))-int(addr_concat,16))
                modified_addr = modified_addr.replace('0x','')
                if len(modified_addr) < 6:
                    for i in range(6-len(modified_addr)):
                        modified_addr = "0"+modified_addr
                address_code[whole_line[1]]    = modified_addr[0] + modified_addr[1]
                address_code[x]                = modified_addr[2] + modified_addr[3]
                address_code[y]                = modified_addr[4] + modified_addr[5]
        print(modified_addr)    
print(address_code)
        

gui_index = list(address_code.values())
data = pd.DataFrame(columns=headerList,index=gui_used)

# Write to CSV file
data.to_csv("Absolute output.csv")
out=pd.read_csv("Absolute output.csv",index_col=[0])

c1=0
k=0
    # for a in range(0,6):
for i in range(len(out.columns)):
        for j in range(len(out.index)):
            h=hex(int(out.columns[i],16)+int(out.index[j],16))
            if c1<len(gui_used):
                if h== hex( int(gui_used[c1],16)):
                    row=j
                    col=i
                    c=0
                    while(c<16):

                     if col==16:
                        row+=1
                        col=0 
                     if col<len(out.columns) :
                        out.iat[row,col]=gui_index[k]

                        col+=1
                        c+=1
                        k+=1 
                    c1+=1
Gui=show(out)
