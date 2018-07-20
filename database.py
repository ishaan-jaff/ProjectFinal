
import psycopg2
#note that we have to import the Psycopg2 extras library!
import psycopg2.extras
import sys

def conn():
    conn_string = "host='localhost' dbname='cms' user='postgres' password='admin'"
    # print the connection string we will use to connect
    #print ("Connecting to database\n	->%s" % (conn_string))

    conn = psycopg2.connect(conn_string)
    return conn

def add1(conn,n,d,l):
    
    print("'"+n+"'","'"+d+"'","'"+l+"'")
    cur = conn.cursor()
    #cursor.execute("INSERT INTO parent values(n,d)",(5,2))
    
    #data = (n,d)
 
    #Squery = ("INSERT INTO parent (serial_id,parent_id) VALUES (%s,%s)"%(data))
    
    
    data = ("'"+n+"'","'"+d+"'","'"+l+"'")
    columnNames ="\"Name\"","\"Description\"","\"wikilinks\""
    
    insert = "INSERT INTO nodes (%s,%s,%s)"%(columnNames)
    values = "VALUES (%s,%s,%s)"%data
 
 

    query = (insert+values)
    
    
    
    #INSERT INTO nodes ("Name","Description","wikilinks") VALUES ('a','c','{a}')
    
    print(query)
    cur.execute(query)
    

    
    conn.commit()
    
    
def getId(conn,nodeName):
    cur = conn.cursor()
    column = "\"Name\""
    query1 = "SELECT * FROM nodes WHERE %s"%column
    nodeName = "'"+nodeName+"'"
    query2 = "= %s"%nodeName
    #print(query1+query2)
    cur.execute(query1+query2)
    
    
    for row in cur:
        return row[0]
     

     

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
       
def getName(conn,nodeId):
    cur = conn.cursor()
    query = "SELECT * FROM nodes WHERE serial_id = %s"%nodeId
    cur.execute(query)
    for row in cur:
        return row[1]
    
    
def getNodeChildren(conn,nodeName):
    cur = conn.cursor()
    Id = getId(conn,nodeName)
    list = getChildrens(conn,Id)
    
    numberOfChildren = len(list)
    children = [ ]
    for x in range (numberOfChildren):
        children.append(getName(conn,list[x]))
    return children 
    
def getNodeParent(conn,nodeName):
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

def readLinks(conn,nodeName):
    cur = conn.cursor()
    Id = getId(conn,nodeName)
    query = "SELECT * FROM nodes where serial_id = %s"%Id
    cur.execute(query)
    links1 = [ ]
    for row in cur:
        links1.append(row[3])
    [links]= links1
    return links

def readValues(conn):
    
    
    
    nodes = [ ]
    cur = conn.cursor()
    query = "SELECT * FROM nodes ORDER BY serial_id"
    cur.execute(query)
    for row in cur:
        
        nodes+=[row]
    return nodes
   