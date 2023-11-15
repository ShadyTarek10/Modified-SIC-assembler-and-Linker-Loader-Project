
import pandas as pd
import re
from pandasgui import show
import itertools
choose=input("Please choose SIC or SICXE ")

if choose=="SIC":
    


    inp = open("SIC_input.txt","r")
    first=inp.readline()
    print(first)
    new=first.split(" ")
    print(new)
    programStart=hex(int(new[2],16))
    programLength=hex(int(new[3],16))
    print(programStart)
    print(programLength)
    endingAddr=hex(int(programLength,16)+int(programStart,16))
    endingAddr=endingAddr.replace('0x','')
    print(endingAddr)


    programList=[]
    trecords=[]
    trecordsaddr=[]
    tlengthlist=[]
    addresses=[]
    headerList=[hex(int('0',16)),hex(int('1',16)),hex(int('2',16)),hex(int('3',16)),hex(int('4',16)),hex(int('5',16)),hex(int('6',16)),hex(int('7',16)),hex(int('8',16)),hex(int('9',16)),hex(int('A',16)),hex(int('B',16)),hex(int('C',16)),hex(int('D',16)),hex(int('E',16)),hex(int('F',16))]
    tcounter=0
    addresses.append(programStart)
    while(programStart<hex(int(endingAddr,16))): # get the program addresses from starting address to ending address 
        programStart=hex(int(programStart,16)+int('16',10))
        addresses.append(programStart)

    for line in inp:
        x=line.split(' ')
        for l in range(0,len(x)): #used to remove white spaces
            x[l]=  x[l].rstrip()
        print(x)
        if line[0]=="M" or line[0]=="D" or line[0]=="R" or line[0]=="E":
            continue
        
        elif line[0]=="T":
            
            tstart=hex(int(x[1],16))
            tlength=hex(int(x[2],16))
            trecordsaddr.append(tstart)
            tlengthlist.append(tlength) 
            for n in range(3,len(x)): # to make list of lists of object codes of every T records and every list of list is seperated intop bytes
                if x[n]=="*":
                    tcounter+=1
                    trecords.append(re.findall('.{1,2}',x[n])) 
                else:
                    trecords.append(re.findall('.{1,2}',x[n]))   

    print(trecords)           
    trecords=list(itertools.chain.from_iterable(trecords)) # to remove list of lists and convert it into one list of bytes  

    print(tcounter)        
    print(trecords)
    print(trecordsaddr)
    print(tlengthlist)
    print(addresses)   


    trecordsaddr1=[]
    c=1
    for i in range(len(trecordsaddr)): #to get the first t record and remove last digit to replace it with 0  
    
        b=int(trecordsaddr[i],16)// int('16',10)
        b=b * int('16',10)
        temp='0'
        if c>0:
          
          c-=1 
          for i in range(len(addresses)): # to get the the rest of ADDRESESS in our memory starting on the first T record address
            
            hamo=b+int(temp,16)
            trecordsaddr1.append(hex(hamo))
            temp=hex(int(temp,16) + int('16',10))
    print(trecordsaddr1) #new trecord addresses


    data = pd.DataFrame(columns= headerList,index=trecordsaddr1) #pandas built in fucntion used to gives values to both axes of csv file
                                                                 #this csv is displayed in our gui   

    # Write to CSV file
    data.to_csv("Absolute output.csv") #generate a csv file and write the contents of columns and indexes 
    out=pd.read_csv("Absolute output.csv",index_col=[0]) #read csv file so it could be used in gui 
    tend=[]
    for i in range(len(trecordsaddr)): # get every T record ending address and store it in tend list
        h=hex(int(trecordsaddr[i],16)+int(tlengthlist[i],16))
        tend.append(h)
    
    print(tend)




    c1=0 # used to count the number of t records loaded and until reaching the amount of T records we have
    counter=16
    k=0 # used as an index of trecords list
    y=0

    for a in range(len(tlengthlist)):  # this part is to load our T records to the memory
        for i in range(len(out.columns)):
            for j in range(len(out.index)):
                h=hex(int(out.columns[i],16)+int(out.index[j],16))
                if c1<len(trecordsaddr): 
                    
                    if h== hex( int(trecordsaddr[c1],16)):
                        row=j # used for incrementing row index if col reached 16 (from 0 to F)
                        col=i # used for start from the first address in columns after incrementing the row
                        m=int(trecordsaddr[c1],16)
                        while  m< int(tend[c1],16):
                            m=m+int('1',10)
                            if col==16:
                                row+=1
                                col=0
                            if col<len(out.columns) :
                                    
                                    out.iat[row,col]=trecords[k]
                                    
                            col+=1      
                            k+=1  
                        c1+=1
                
    Gui=show(out) #show csv file on pandasGUI

elif choose=="SICXE":
    

    headerList=[hex(int('0',16)),hex(int('1',16)),hex(int('2',16)),hex(int('3',16)),hex(int('4',16)),hex(int('5',16)),hex(int('6',16)),hex(int('7',16)),hex(int('8',16)),hex(int('9',16)),hex(int('A',16)),hex(int('B',16)),hex(int('C',16)),hex(int('D',16)),hex(int('E',16)),hex(int('F',16))]

    num_of_progs = int(input("Please Enter Number of Programs:"))
    print("Please Enter The Sequence of Programs:")
    Seq_of_progs = []
    Trecords     = []
    ESTAB_values={}
    address_code={}
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
        # for line in current_prog2.readlines():
        #     estab_file.writelines(line)
        #     cur_line=line.split()
        #     if(cur_line[0] == 'T'):
        #         for n in range(3,len(cur_line)):
        #             Trecords.append(re.findall('.{1,2}',cur_line[n]))


    estab_file.close()
    Relocation = input("please enter the starting value in hex:")
    estab_file = open("estabgen.txt","r")
    for line in estab_file.readlines():
        whole_line = line.split()
        if (whole_line[0] == "H"):
            name=whole_line[1]
            if len(name) < 6:
                        for i in range(6-len(name)):
                            name =  name+"x"
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
                    if len(Dname) < 6:
                        for i in range(6-len(Dname)):
                            Dname =  Dname+"x"
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
    gui_index = list(address_code.values())
            


    print(gui_used)
    print(gui_index)




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

    print(address_code)
    # print(ESTAB_values)






    # check_len = check_len.replace('0x','')
            # if len(check_len) < 6:
            #             for i in range(6-len(check_len)):
            #                 check_len = "0"+check_len
            # addr_diff = addr_diff.replace('0x','')
            # if len(addr_diff) < 6:
            #             for i in range(6-len(addr_diff)):
            #                 addr_diff = "0"+addr_diff