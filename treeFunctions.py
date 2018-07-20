
### All trees used in UI.py are managed here, the front end of the trees are managed here 


### Modules used
try:
    # for Python3
    from tkinter import*
except ImportError:
    # for Python2
    import Tkinter as tk
    

## Project Files used 
from search_PopUp import*
try:# Python 3
    from tkinter import ttk
except:#Python 2
    from Tkinter import Ttk
from databaseFunctions import*



duplicates = dict()


### Global variable deals with nodes having more than one parent 
count=1


    
##This function is caled in UI.py to update the tree dealing with nodes 
def updateTree(root,tree,name,description,links,parent):
    
    #If a node exists in the tree
    if tree.exists(name)==True:
        
        
        global count 
        name = name+ ((" ")*count)
        # this is a work around, you can not insert the same element in a tree/ no duplicates can be present 
        #It it is a duplicate then white space is added 
        # when user clicks/updates node, name = nodeName.strip() can be seen in UI.py, this is to deal with this whitespace 
        insertNodeUi(tree,name,parent,description)
        
        count+=1# increment amount of whiteSpace 
    
        #Use this to debug
        #print("item exist update"+name)
        
    elif name == parent:# Only in the case of Search, Search is its own parent 
               
        insertNodeUi(tree,name,"",description)
    else:
        # all other cases 
        insertNodeUi(tree,name,parent,description)
   
   
   
### If a tree only needs to be updated to show new data entered 
# This updates a particular node, nodename,description etc 

def updateT(root,tree,name,newName,description,links):
    
    tree.item(name, text=newName, values=(description,links))
    
   
    

## Make the Nodes Tree, this is called in UI.py
def makeTree(root,conn,tree):
    
    # get users screen info 
    screen_width = int(root.winfo_screenwidth())
    screen_height = int(root.winfo_screenheight())


    tree["columns"]=("one")
    tree.column("one", width=int(screen_width/5) )
    tree.heading("one", text="Description")
   
   
    nodes = (readValues(conn()))# this a a function in databaseFunctions.py
    
    
    for node in nodes:
        name,description = node[1],node[2]
        if name ==None:
            continue 
        parent = getNodeParent(conn(),name)# this a a function in databaseFunctions.py
        
        if len(parent) ==1:
            parentName = parent[0]
            if name == parentName:
                insertNodeUi(tree,name,"",description)
            else:
                insertNodeUi(tree,name,parentName,description)
        else: #More than one parents 
            print(name,parent)
            
            for x in range(len(parent)): # to deal with nodes having more than one parent 
               
                parentName = parent[x]
                if tree.exists(name)==True:
                    
                    name = name+ ((" ")*x) #this is a work around, you can not insert the same element in a tree/ no duplicates can be present 
        #If it is a duplicate then white space is added 
        # when user clicks/updates node, name = nodeName.strip() can be seen in UI.py, this is to deal with this whitespace 
        
        
        
        
                    try:
                        insertNodeUi(tree,name,parentName,description)
                    except:
                        continue 
            
                else:
                    try :
                        insertNodeUi(tree,name,parentName,description)
                    except:
                        continue
            
    
  
    




### Just to add conn
def drawTree(root,tree):
    makeTree(root,conn,tree)

## Get links for selected node 
def getNodeLinks(nodeName):
 
    getNodeChildren(conn(),nodeName) # references a database Function




### This function does the insertion into the main Nodes Tree 
def insertNodeUi(tree,nodeName="",nodeParent="",description=""):
   
    try:
        tree.insert(nodeParent,1,nodeName,text = nodeName,values=description)
   
    except:
        print("One Error")
        






