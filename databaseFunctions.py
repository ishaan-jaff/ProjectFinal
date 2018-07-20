

## psycopyg is used to make the connection to the db
import psycopg2
#note that we have to import the Psycopg2 extras library!
import psycopg2.extras



import json 
from linksManager import*


## Function to make connection to Database 
## Will need to be updated to new host, dbname, user and password 
def conn():
    conn_string = "host='localhost' dbname='cms' user='postgres' password='admin'"
    conn = psycopg2.connect(conn_string)
    return conn


## Function to update a particular node in the DB 
def updateData(conn,name):# UPDATE data in database 
    links,meta = readLinks(conn,name)
    newMeta=[[]]
    newMeta = convert(links)
    insertMetadata(conn,name,newMeta)# this is a function in databaseFunctions.py
    
## To get serial_id of nodeName 

def getId(conn,nodeName):
    cur1 = conn.cursor()
    column = "\"Name\"" # String formatting for Postgress 
    query1 = "SELECT * FROM nodes WHERE %s"%column
    nodeName = "'"+nodeName+"'"
    query2 = "= %s"%nodeName
    cur1.execute(query1+query2)
    for row in cur1:
        return row[0]  # row[0[ is the serial_id of the list 
         

## Function handles inserting, updating data for links for a prticular node
## deals with links_metadata

def insertMetadata(conn,nodeName,metaData):
    cur = conn.cursor()
    id =  getId(conn,nodeName)
    queryValues=""
    
    #LOOPS through link,name,date,attachments for each link 
    for x in range(len(metaData)):
        
        
        # if there are two elements, i.e no attachments for a particualr link then attachments=[]
        if len(metaData[x]) == 3:
            metaData[x].append([])
        try:
            link,name,date,attachments = metaData[x][0],metaData[x][1],metaData[x][2],str(metaData[x][3]).replace("'","")
        
        except:
            print(metaData[x])
        
        
        
         # edge case, add no comma to query if last json object or only one JSON 
        if x == len(metaData)-1:
            json_data = "\'{ \"link\": \"%s\", \"title\": \"%s\",\"date\":\"%s\",\"attachments\":\"%s\"}\'"%(link,name,date,attachments)
            
            # in the db the column names include double quotes for some reason, so whe inserting it #has to insert into "link", "title" .. 
        
        
        
        else:# comma exists at the end of json_data in this case 
        
            json_data = "\'{ \"link\": \"%s\", \"title\": \"%s\",\"date\":\"%s\",\"attachments\":\"%s\"}\',"%(link,name,date,attachments)
        queryValues+=json_data
    
    
    query = ("update public.nodes set \"links_metadata\" = cast((array[%s]) as json[]) where \"Name\"=\'%s\'")%(queryValues,nodeName)
    
    
    query  = query.replace('\n', ' ').replace('\r', '')
    cur.execute(query)
    conn.commit()

## use this to debug the function
#insertMetadata(conn(),"Search",[["HI","SS","NOC",[{"A":"S"},{"https:":"dd"},[]]],["LLL","KK","2018"]])





## Add data to nodes table 
## insert name,desription and metaData is all metadata for links of that node 
def addToNodes(conn,n,d,metaData):
    cur = conn.cursor()
    data = ("'"+n+"'","'"+d+"'") # the data needed single quotes when entered 
    columnNames ="\"Name\"","\"Description\"" # column names need to be represented as "Name" not # #just Name , they need to have double quotes in the query 
    
    
    
    insert = "INSERT INTO nodes (%s,%s)"%(columnNames)
    values = "VALUES (%s,%s)"%data
    query = (insert+values)
    cur.execute(query)
    conn.commit()
    insertMetadata(conn,n,metaData)# this calls the function above, insertMetadata

## use this to debug this function 
#addToNodes(conn(),"Search123","Discovery",[["https","Data","NOV"],["hhtt","Data","Dsm"]])
   
   
   
   
## Add data to parents table 
## Creates parent child relationships 
def addToParent(conn,name,parentName):
    cur = conn.cursor()
    serial_id = getId(conn,name) # id of current node, user only gives name of node
    parent_id = getId(conn,parentName) # id of parent
    if (parent_id==None): # if the user gives a parent name that does ot exist
        return None
    data = (serial_id,parent_id)
    query = ("INSERT INTO parent (serial_id,parent_id) VALUES (%s,%s)"%(data))
    cur.execute(query)
    conn.commit()

## use this to debug this function
#print(addToParent(conn(),"amaz","Tools"))


## Get children for a particular node, this is used in the front end, when displaying all the node names
## this function only gets the serial_id of children 
def getChildrens(conn,nodeId):
    cur = conn.cursor()
    query = "SELECT * FROM parent WHERE parent_id = %s"%nodeId
    cur.execute(query)
    list1 = [ ]
    for row in cur:
        list1.append(row[1])
        set1 = set(list1)
        childList =list(set1) 
        
    return childList
 
 
 
 
## Based on the ID get the name of the node correponding to the serial_id
def getName(conn,nodeId):
    cur = conn.cursor()
    query = "SELECT * FROM nodes WHERE serial_id = %s"%nodeId
    cur.execute(query)
    for row in cur:
        return row[1]
    
    
## This returns a list of all children of a node, it uses getName and getChildrens. 
def getNodeChildren(conn,nodeName):
    cur = conn.cursor()
    Id = getId(conn,nodeName)
    list = getChildrens(conn,Id)
    
    numberOfChildren = len(list)
    children = [ ]
    for x in range (numberOfChildren):
        children.append(getName(conn,list[x]))
    return children 
    
    

## gets Id of node, based on that gets parentID, after that gets parentName 
def getNodeParent(conn,nodeName):
    if nodeName==None:
        return None
    cur = conn.cursor()
    Id = getId(conn,nodeName)    
    query = "SELECT * FROM parent WHERE serial_id = %s"%Id
    cur.execute(query)
    parent = []
    for row in cur:
        parent.append(row[2])
    parentName=[]
    for element in parent:
        parentName.append(getName(conn,element))
    
    return parentName




## This function returns the ParentName of a Node, it is used in the SearchPopUp to see the path of a partciular node 
def getParentName(conn,nodeName):
    if nodeName==None:
        return None
   
    cur = conn.cursor()
    Id = getId(conn,nodeName)
    query = "SELECT * FROM parent WHERE serial_id = %s"%Id
    cur.execute(query)
    parent = []
    for row in cur:
        parent.append(row[2])
  
    for element in parent:
        #print(getName(conn,element))
        if getName(conn,element)!=None:
            
            return getName(conn,element)
        else:
            return None 
  
  
## use this to debug this function
#print(getParentName(conn(),"Architecture"))
    
   
    
    
    
    
## This is used in the SearchPopUp to get the path of a node 
## uses getParentName 
def getPath(conn,nodeName,path=""):# recursive function to get path
    if getParentName(conn,nodeName)==None:
        return None
    if getParentName(conn,nodeName)==nodeName:#base case
        path+=nodeName
        return (path)
    else:#recursive case 
        path+=nodeName+"->"
        parent=getParentName(conn,nodeName)
        return getPath(conn,parent,path)
        
        
#print(getPath(conn(),"Search Architecture"))
#print(getNodeParent(conn(),"Search"))




## Reads links_metaData on the basis of a nodeName
def readLinks(conn,nodeName):
    #print(nodeName)
    cur = conn.cursor()
    Id = getId(conn,nodeName)
    print(Id)
    try:
        query = "SELECT \"links_metadata\" FROM nodes where serial_id = %s"%Id
        cur.execute(query)

    except:
        query = "SELECT \"links_metadata\" FROM nodes where \"Name\" = \'%s\'"%nodeName.strip()
        cur.execute(query)

        
    list=[]
    links=[]
    metaData = [] 
    
    for row in cur:
        list = (row[0])
    
    if list!= None:
        for element in list:
            if element['link'].replace(" ","")!="":# only if links is not "" then it should read it 
                
                #links is used mainly for the front end 
                links.append(element['link'])
                
                # this has information about links, title, date attachment 
                # metaData is a 2d list 
                #[[https://spaces.telenav.com,Space,Nove-2018,[{https://:attachment},[1,2,3],{}]]]
                metaData.append([element['link'],element['title'],element['date'],element['attachments']])
                
            
    else:
        return [],[[]]

    return links,metaData
    
## USe this to debug, use appropriate existing node name 
#print(readLinks(conn(),"Search"))








## Read all data for a node 
def readRow(conn,nodeName):
    cur = conn.cursor()
    Id = getId(conn,nodeName)
    if Id==None:
        return None 
    query = "SELECT * FROM nodes where serial_id = %s" %Id
    cur.execute(query)
    for row in cur:
        return row
## use this to Debug this function
#print(readRow(conn(),"Search"))



## Called when the update a node or update selected node option is selected 
def update(conn,nodeName,newName,description,metaData):
    cur = conn.cursor()
    Id = getId(conn,nodeName)
    data1=("\"Name\"","'"+newName+"'","\"Description\"","'"+description+"'")
    data2 = (Id)
    
    query1 = "UPDATE nodes SET %s = %s, %s=%s"%data1
    query2 = "WHERE serial_id = %s"%data2
    try:
        cur.execute(query1+query2)
        conn.commit()
    except:
        query3 = "WHERE \"Name\" = \'%s\'"%nodeName
        cur.execute(query1+query3)
        conn.commit()
        
    
    insertMetadata(conn,newName,metaData)# function in databaseFunctions.py
    
## use this to debug this function 
#update(conn(),"Search","Search","i",[["htt","dd","L"]])





## When add link/links button is clicked 
## first reads all the links for a node, add the new links to the existing metadata and then inserts it 
## for new links when they are added only link is added, title,date, attcahments are blank, ==""

def addLinks(conn,nodeName,wikilink):
    
    cur = conn.cursor()
    newLinks=[]
    links = []
    oldLinks=[]
    list=None
    query = "SELECT links_metadata FROM nodes where \"Name\" = \'%s\'" %nodeName
    cur.execute(query)
    for row in cur:
        list = (row[0])
    if list!= None and list!=[[]]:
        for element in list:
                
            links.append([element['link'],element['title'],element['date']])
            oldLinks.append(element['link'])
    
    for link in wikilink:
        links.append([link,"",""]) # new links added have "" as title ,date 
    
    insertMetadata(conn,nodeName,links)# this is the main function of addLinks 
    
    
    return oldLinks# this is not the main fucntion of addLinks but helps with the front end, this oldLinks helps update UI.py 
    
## Use this to debug this function 
#print(addLinks(conn(),"Search",["https://www.cmu.andrew.edu.com"]))
    


def readValues(conn):
    nodes = [ ]
    cur = conn.cursor()
    query = "SELECT * FROM nodes ORDER BY serial_id"
    cur.execute(query)
    for row in cur:
        
        nodes+=[row]
    return nodes
#print(readValues(conn()))

def readAllLinks(conn):
    nodes = [ ]
    cur = conn.cursor()
    
    
    
    query = "SELECT * FROM nodes ORDER BY serial_id"
    cur.execute(query)
    for row in cur:
        
        nodes+=[row[3]]
    return sum(nodes,[])

    
#print(readAllLinks(conn()))


def getLinks(conn):
    links=[]
    names=[]
    frontEndLinks=[]
    metaData=[[]]
    linksAndText = dict()
    cur = conn.cursor()
    query = "SELECT links_metadata FROM nodes ORDER BY serial_id"
    column = "\"Name\""
    query1 = "SELECT %s FROM nodes"%column
    cur.execute(query)
    
    for row in cur:
        links.extend(row)
    for element in links:
           
        if element!=None and element!=[] :
            data = element[0]
            if (data['link'].find("pageId=")!=-1):
                frontEndLinks.append(data['title'])
                linksAndText[data['title']] = data['link']
            else:
                frontEndLinks.append(data['link'])
                linksAndText[data['title']] = data['link']
            #metaData.append([data['link'],data['title'],data['date']])
    
    

    #To get all Node Names 
    cur.execute(query1)
    for row in cur:
        names+=row 
        
    return frontEndLinks,names,linksAndText
    
def getAttachments(conn,link,nodeName):
    if link==None:
        return None 
    
    cur = conn.cursor()
    links,meta = readLinks(conn,nodeName)
    
    for data in meta:
        if data[0] == link:
            if len(data)==3:
                return []
            else:
                return (data[3])
#print(getAttachments(conn(),"HI","Search"))
    
    
    
#print(getLinks(conn()))





    
    
    
        
        
    
    
    