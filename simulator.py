import xlrd


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


class root:
    def __init__(self):
        self.prefix="root"

class prefixnode:
    def __init__(self,mylist):
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
loc = ("routingtable.xls")
 
# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
 
for i in range(sheet.nrows):
    listofips.append(prefixnode(sheet.row_values(i)))


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




def getnexthop(index,listofips,address):
    matchlen=0
    for i in range(len(listofips[index].prefix)+1):
        if(listofips[index].prefix[:i]==address[:i]):
            matchlen=i
    while(str(matchlen) not in listofips[index].nexthopdict.keys() and matchlen>0):
        matchlen-=1
    if(matchlen==0):
        print("The default gatway is next hop\n")
    else:
        nexthop=listofips[index].nexthopdict[str(matchlen)]
        print("matched with: ",listofips[index].prefix[:matchlen]," ","the next hop is : ",nexthop)
    
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
    print(i,"-",listofips[i].prefix)
print("-------------")
print("list of leaves:")
for i in range(len(listofleaves)):
    print(i,"-",listofleaves[i].prefix)
print("-------------")
# testcase="01101111000011110000111100001111"  next hop is 8
# testcase="10110111000000000000000000000000"  next hop is 2
# testcase="10111111000000000000000000000000"  next hop is 8
# testcase="10100001000000000000000000000000"  next hop is 3
# testcase="11110111000000000000000000000000"  next hop is default gatway
# testcase="10000111000000000000000000000000"  next hop is 3

while(True):
    choice=input("1-searching for address\n2-searching for address(disjoint)\n3-exit\n")
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
    else:
        break

