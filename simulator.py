import xlrd
import xlwt
import sys
import time
from xlutils.copy import copy

def comparision(prefix1,prefix2):
	if(len(prefix1)==len(prefix2)):
		if(prefix1==prefix2):
			return "eq"
		if(prefix1>prefix2):
			return "gt"
		else:
			return "lt"
	else:
		if(len(prefix1)>len(prefix2)):
			if(prefix1[:len(prefix2)]<=prefix2):
				return "lt"
			else:
				return "gt"
		else:
			if(prefix2[:len(prefix1)]<=prefix1):
				return "gt"
			else:
				return "lt"


def binarySearch (arr, l, r, x): 
    if r >= l: 
        mid = l + (r - l) // 2
        if arr[mid].prefix == x: 
            return mid,"found"
        elif comparision(arr[mid].prefix,x)=="gt": 
            return binarySearch(arr, l, mid-1, x) 
        else: 
            return binarySearch(arr, mid + 1, r, x) 
    else:
        return l,"failed"

def hex2bin(hexval): 
    value = int(hexval, 16) 
    bindigits = [] 
     
    # Seed digit: 2**0 
    digit = (value % 2) 
    value //= 2 
    bindigits.append(digit) 
     
    while value > 0: 
        # Next power of 2**n 
        digit = (value % 2) 
        value //= 2 
        bindigits.append(digit) 
         
    return ''.join([str(d) for d in bindigits])



class root:
    def __init__(self):
        self.prefix="root"

class prefixnode:
    def __init__(self,mylist,base):
        if(base==16):
            if(type(mylist[0])==float):
                mylist[0]=int(mylist[0])
            mylist[0]=str(mylist[0])
            mylist[0]=hex2bin(mylist[0])[::-1]
            while(len(mylist[0])!=32):
                mylist[0]="0"+mylist[0]
            mylist[0]=mylist[0][:int(mylist[1])]
            mylist=[mylist[0]+"*",int(mylist[2])]
        self.prefix=mylist[0][:-1]
        self.nexthopdict={str(len(self.prefix)):int(mylist[1])}  #pathinformation
        self.nexthop=int(mylist[1])
        self.parent=root()
        self.children=[]
        self.isleaf=0
    def __str__(self):
        return self.prefix

listofips=[]

# Give the location of the file
location=input("please enter the path of routing table:\n")
loc = (location)

base=int(input("routing table is base of 2 or 16:\n"))

# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
 

start_time = time.time_ns()

for i in range(sheet.nrows):
    listofips.append(prefixnode(sheet.row_values(i),base))

#sort routing enteries

for i in range(len(listofips)):
    for j in range(i,len(listofips)):
        if(comparision(listofips[i].prefix,listofips[j].prefix)=="gt"):
            listofips[j],listofips[i]=listofips[i],listofips[j]

# #sort routing enteries
listofleaves=[]
# #finding parents
for i in range(len(listofips)):
    if(len(listofips[i].children)==0):
        listofips[i].isleaf=1
    for j in range(i,len(listofips)):
        if(len(listofips[j].prefix)<len(listofips[i].prefix)):
            if(listofips[j].prefix==listofips[i].prefix[:len(listofips[j].prefix)] and listofips[i].parent.prefix=="root"):
                listofips[i].parent=listofips[j]
                listofips[j].children.append(listofips[i])
#setting pathinformation
for i in listofips:
    temp=i.parent
    while(temp.prefix!="root"):
        i.nexthopdict[str(len(temp.prefix))]=temp.nexthop
        temp=temp.parent
    if(i.isleaf==1):
        listofleaves.append(i)

timetobuild=time.time_ns() - start_time

def getnexthop(index,listofips,address):
    matchlen=0
    for i in range(len(listofips[index].prefix)+1):
        if(listofips[index].prefix[:i]==address[:i]):
            matchlen=i
    while(str(matchlen) not in listofips[index].nexthopdict.keys() and matchlen>0):
        matchlen-=1
    if(matchlen==0):
        print("The default gatway is next hop\n")
        return "default gayway"
    else:
        nexthop=listofips[index].nexthopdict[str(matchlen)]
        print("matched with: ",listofips[index].prefix[:matchlen]," ","the next hop is : ",nexthop)
        return str(nexthop)
    
def getnexthopdis(index,listofleaves,address):
    matchlen1=0
    matchlen2=0
    for i in range(len(listofleaves[index].prefix)+1):
        if(listofleaves[index].prefix[:i]==address[:i]):
            matchlen1=i


    if(index-1>=0):
        for i in range(len(listofleaves[index-1].prefix)+1):
            if(listofleaves[index-1].prefix[:i]==address[:i]):
                matchlen2=i

    while(str(matchlen1) not in listofleaves[index].nexthopdict.keys() and matchlen1>0):
        matchlen1-=1

    while(str(matchlen2) not in listofleaves[index-1].nexthopdict.keys() and matchlen2>0):
        matchlen2-=1

    if(matchlen1==0 and matchlen2==0):
        print("The default gatway is next hop\n")
    elif(matchlen1>matchlen2):
        nexthop=listofleaves[index].nexthopdict[str(matchlen1)]
        print("matched with: ",listofleaves[index].prefix[:matchlen1],"and the next hop is : ",nexthop)
    else:
        if(index-1>=0):
            nexthop=listofleaves[index-1].nexthopdict[str(matchlen2)]
            print("matched with: ",listofleaves[index-1].prefix[:matchlen2],"and the next hop is : ",nexthop)
        


print("list of prefixes:")
for i in range(len(listofips)):
    print(i+1,"-",listofips[i].prefix)
print("-------------")
print("list of leaves:")
for i in range(len(listofleaves)):
    print(i+1,"-",listofleaves[i].prefix)
print("-------------")
print("number of entries: ",len(listofips))
print("size of structure:(all nodes)")
print(sys.getsizeof(listofips)," Bytes")
print("size of structure:(only leaves)")
print(sys.getsizeof(listofleaves)," Bytes")
print("time to build structure: ",timetobuild," nanoseconds")
# testcase="01101111000011110000111100001111"  next hop is 8
# testcase="10110111000000000000000000000000"  next hop is 2
# testcase="10111111000000000000000000000000"  next hop is 8
# testcase="10100001000000000000000000000000"  next hop is 3
# testcase="11110111000000000000000000000000"  next hop is default gatway
# testcase="10000111000000000000000000000000"  next hop is 3

while(True):
    choice=input("1-searching for address\n2-searching for address(disjoint)\n3-select csv file and analyse\n4-exit\n")
    if(choice=="1"):
        address=input("please enter the 32 bit ip address:\n")
        index,status = binarySearch(listofips, 0, len(listofips)-1,address)
        if(status=="found"):
            print("the next hop is : ",str(listofips[index].nexthop))
        elif(index==len(listofips)):
            print("The default gatway is next hop\n")
        else:
            getnexthop(index,listofips,address)
    elif(choice=="2"):
        address=input("please enter the 32 bit ip address:\n")
        index,status = binarySearch(listofleaves, 0, len(listofleaves)-1,address)
        if(status=="found"):
            print("the next hop is : ",str(listofleaves[index].nexthop))
        elif(index==len(listofleaves)):
            print("The default gatway is next hop\n")
        else:
            getnexthopdis(index,listofleaves,address)
    elif(choice=="3"):
        path=input("please enter path of csv file:(base of tests should be 16)\n")
        loc2 = (path)
        # To open Workbook
        wb2 = xlrd.open_workbook(loc2)
        sheet2 = wb2.sheet_by_index(0)
        w = copy(wb2)
        choice2=input("1-binary search 2-binary search using disjoint prefixes\n")
        start=time.time_ns()
        if(choice2=="1"):
            for i in range(sheet2.nrows):
                if(type(sheet2.row_values(i)[0])==float):
                    address=hex2bin(str(int(sheet2.row_values(i)[0])))[::-1]
                else:
                    address=hex2bin(str(sheet2.row_values(i)[0]))[::-1]
                while(len(address)!=32):
                    address="0"+address
                index,status = binarySearch(listofips, 0, len(listofips)-1,address)
                if(status=="found"):
                    w.get_sheet(0).write(i,1,str(listofips[index].nexthop))
                elif(index==len(listofips)):
                    w.get_sheet(0).write(i,1,"default gatway")
                else:
                    w.get_sheet(0).write(i,1,getnexthop(index,listofips,address))
        else:
            for i in range(sheet2.nrows):
                if(type(sheet2.row_values(i)[0])==float):
                    address=hex2bin(str(int(sheet2.row_values(i)[0])))[::-1]
                else:
                    address=hex2bin(str(sheet2.row_values(i)[0]))[::-1]
                while(len(address)!=32):
                    address="0"+address
                index,status = binarySearch(listofleaves, 0, len(listofleaves)-1,address)
                if(status=="found"):
                    w.get_sheet(0).write(i,1,str(listofleaves[index].nexthop))
                elif(index==len(listofleaves)):
                    w.get_sheet(0).write(i,1,"default gatway")
                else:
                    w.get_sheet(0).write(i,1,getnexthop(index,listofleaves,address))
        w.save('answer.xls')
        end=time.time_ns()
        print("\n\n\n\n\n\n\n\n\n\n\n")
        print("number of entries: ",sheet2.nrows)
        print("execution time: ",end-start," nanoseconds")
    else:
        break
