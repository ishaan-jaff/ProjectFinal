
from tkinter import *
from tkinter import ttk
from databaseFunctions import*
from widget import*


#from pract import *
import webbrowser
#from UI import *


#from read import*





def callback(event):
    webbrowser.open_new(r"http://www.google.com")
    





"""def selectItem(tree):
    curItem = tree.focus()
    print (tree.item(curItem))"""
    
    

def makeTree(root,conn):
    screen_width = int(root.winfo_screenwidth())
    screen_height = int(root.winfo_screenheight())

    tree = ttk.Treeview(root)
    
    tree["columns"]=("one")
    tree.column("one", width=int(screen_width/4) )
    
    tree.heading("one", text="Description")
    #insertNode(tree)
    nodes = (readValues(conn()))
    #insertNode(tree)
    #print(nodes)
    
    for node in nodes:
        print(node)
        name,description = node[1],node[2]
        #print(name)
        
        parent = getNodeParent(conn(),name)
        

        
        
        if len(parent) ==1:
            parentName = parent[0]
            if name == parentName:
                print("reached here")
                insertNodeUi(tree,name,"",description)
            else:
                insertNodeUi(tree,name,parentName,description)
        else:
            for element in parent: # to deal with nodes having more than one parent 
                parentName = element
                insertNodeUi(tree,name,parentName,description)
    
    tree.bind("<Button-1>", OnDoubleClick(tree))
    tree.pack(side = LEFT)

    
    
    #tree.bind("<Button-1>", OnDoubleClick(event))
    
    """"#link = Label(root, text="Google Hyperlink", fg="blue", cursor="hand2")
    #link.pack()
    link = Label(root, text="Google Hyperlink", fg="blue", cursor="hand2")
    insertNodeUi(tree,"""





def drawTree(root):
    makeTree(root,conn)
    


def insertNodeUi(tree,nodeName="",nodeParent="",description=""):
    #print(nodeParent,1,nodeName,text = nodeName,values=description)
    tree.insert(nodeParent,1,nodeName,text = nodeName,values=description)

def OnDoubleClick(event=None,tree=None):
    item = tree.identify("item", event.x, event.y)
    print ("you clicked on", tree.item(item)["text"])
    

"""def insertNode(tree):
    tree.insert(" ", 0, "Search", text="Search",values="hi")
    tree.insert("Search",1,"Data Architecture", text="Data Architecture",values=(""))
    
    tree.insert("Architecture",1446,"Search Architecture", text="Search Architecture",values=(""))
    tree.insert("Architecture",1,"Data Architecture", text="Data Architecture",values=(""))
    #tree.insert("Architecture", 'end', text="Arch",values=(""))
    tree.insert("Search", 0, text=" sjjj",values=(""))
    tree.insert("Search", 0, text=" sjjj",values=(""))
    tree.insert("Search", 0, text=" sjjj",values=(""))
   
    
    id2 = tree.insert("", 1, "dir2", text="Dir 2")
    tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))
    
    ##alternatively:
    tree.insert("", 3, "dir3", text="Dir 3")
    tree.insert("dir3", 3, text=" sub dir 3",values=("3A"," 3B"))"""

    








