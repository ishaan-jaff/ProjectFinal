############################
###########################

###        THIS IS THE MAIN FILE, RUN THIS TO RUN THE APPLICATION/CMS





## tkinter should already exist on python, I have used python 3.6.5

try:
    # for Python3
    from tkinter import*
except ImportError:
    # for Python2
    import Tkinter as tk
try:# Python 3
    from tkinter import ttk
except:#Python 2
    from Tkinter import Ttk
    

    
  
  
  
### These are the files that are in the cms folder, they are used by UI.py
## I have written these files

from search_PopUp import*
from treeFunctions import*
from scraper import*
from databaseFunctions import*
from linksManager import*
from attachmentsPopUp import*
from listBoxMaker import*
from hoverBoxes import*


## re, is Regex for Python, this is used for the search engine
import re

    
## May need to pip install PIL to see image of Logo
## pip install PIL works well
from PIL import ImageTk, Image

## this is used to spped up homescreen mouse pressed
## will need to install cachetools for python 
## pip install cachetools works well
from cachetools import cached, TTLCache  # 1 - let's import the "cached" decorator and the "TTLCache" object from cachetools
cache = TTLCache(maxsize=100, ttl=300) 



## comes with python, used to open weblinks 
import webbrowser





####################################
# init this is the main variables used 
####################################


## Creaitng a Tkinter window
root = Tk()

## this is a frame in the window
## all widgets are placed on frame 
frame = Frame(root)
frame.pack()

## to get users screen width and height 
screen_width = int(root.winfo_screenwidth())
screen_height = int(root.winfo_screenheight())



####
###   Used to initialise variables 

def init(data,frame):
    # mode is always homeScreen
    data.mode = "homeScreen"
    
    # data.tw is used for the hoverBoxes
    data.tw=""
    
    
    data.nodeClicked = ""
    
    #Trees used
    #data.tree is the tree on the left side, with node names and descriptions
    data.tree = tree = ttk.Treeview(frame,height=18)
    drawTree(frame,data.tree)
    data.tree.tag_configure('focus')
    data.tree.bind("<Motion>",lambda event, arg=data: mycallback_Tree(event,data,arg))
    data.last_focus_tree=None
    data.tree.grid(row=2,rowspan=2,column=0,columnspan=3)
    
    # tree1 is used in the searchPopUp to show node names and paths
    data.tree1 = ttk.Treeview("",height=10,columns=("A"))

    # treeBox is the tree with all links 
    data.treeBox = ttk.Treeview(frame,height=18,columns=("A","B"))
    data.treeBox.tag_configure('focus', background='yellow')
    data.treeBox.bind("<Motion>",lambda event, arg=data: mycallback(event,data,arg))
    data.last_focus=None
    data.treeBox.heading("#0", text="Nodes Links")
    data.treeBox.heading("A", text="Last Modified")
    data.treeBox.heading("B", text="Attachments")
    data.treeBox.column("#0",width = int(screen_width/7))
    data.treeBox.column("A",width=int(screen_width/8))
    data.treeBox.column("B",width=int(screen_width/10) )
    data.treeBox.grid(row=2,rowspan=2,column=4,columnspan=3)
    
   
    data.links = [ ]
    data.linksDict = dict()
    data.newMeta = []
    
    
    data.updateServiceTime = 0
    
    
    
    #---------------------------------------------------------------------------------------------#
    ##Buttons used 
    
    
    data.addButton = Button(frame,text = "Add a new Node",relief=RAISED)
    data.addButton.grid(row=6,column=0)
    
    data.updateButton = Button(frame,text="Update a Node", relief =RAISED)
    data.updateButton.grid(row=6,column=1)
    
    data.updateSelectedButton=Button(frame,text="Update Selected Node",relief=RAISED)
    data.updateSelectedButton.grid(row=4,column=1)
    
    
    # add child for selected node button
    data.addSelectedButton = Button(frame,text="Add Child for Selected Node",relief=RAISED)
    data.addSelectedButton.grid(row=4,column=0)
    
    data.addLinkButton = Button(frame,text="Add link for selected node", relief =RAISED)
    data.addLinkButton.grid(row=6,column=9,columnspan=2)
    
    data.searchButton = Button(frame,text="Search"  ,relief=RAISED)
    data.searchButton.grid(row=1,column=9)
    
    
    data.addFlag=False 
    data.twFlag = False
    
    #---------------------------------------------------------------------------------------------#
    #Entry Boxes 
    
    data.searchEntry = Entry(frame,width=58)
    data.searchEntry.grid(row=1,column=4,columnspan=3)
    
    data.linkEntry= Entry(frame,width=58)
    data.linkEntry.grid(row=6,column=4,columnspan=3)
    
    Label(frame, text="If you want to enter more than one link seperate them with a \",\"",font="Myriad 15").grid(row=8,column=4,columnspan=3)
    data.htmlLink=""
    
    
    
    # Image of logo shown on home page 
    path1 = "/Users/ishaanj/Desktop/Project/image.jpg"
    img1 = ImageTk.PhotoImage(Image.open(path1))
    panel1 = Label(frame, image = img1)
    panel1.image=img1
    panel1.grid(row=1,column=0,columnspan=3)
    
    
    
    data.updateNodeName =""
    data.updateFlag=False 
    data.updateLinkFlag = False 
    data.oldLinks=[]
    data.conn=""

    
   
    

   


####################################
# mode dispatcher 
####################################

# There is only one mode homeScreen 

def mousePressed(event, data):
    if (data.mode == "homeScreen"): homeScreenMousePressed(event, data)
   
def keyPressed(event, data):
    if (data.mode == "homeScreen"): homeScreenKeyPressed(event, data)
    
def timerFired(data):
    if (data.mode == "homeScreen"): homeScreenTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "homeScreen"): homeScreenRedrawAll(canvas, data)
    

####################################
# homeScreen mode
####################################

### This is the only mode 



### Functions 




### function to update front end display of links for a node 
def updateLinks(data):
    #delete everything from treeBox
    data.treeBox.delete(*data.treeBox.get_children())
    if data.newMeta!=[[]] and data.newMeta!=[]:
        for x in range (len(data.newMeta)):
            linkText,date = data.newMeta[x][1],data.newMeta[x][2]
            if linkText.replace(" ","")=="" or linkText=="":
                linkText = data.newMeta[x][0]
            try:
                data.treeBox.insert("",1,linkText,text=linkText,values=(date,"Attachments"))
            except:
                linkText = linkText + (x*" ")
                data.treeBox.insert("",1,linkText,text=linkText,values=(date,"Attachments"))




## Command if user wants to add a node 
def addCommand(data):# If user wants to add a node 
    
    master = Tk() 
    
    # to make a new popup screen 
    #---------------------------------------------------------------------------------------------#
    #Labels used in popup 
    #These are the field names 
    Label(master, text="Node Name").grid(row=0)
    Label(master, text="Parent Name").grid(row=1)
    Label(master, text="Description").grid(row=3)
    Label(master, text="Links").grid(row=4)
    
    
    #---------------------------------------------------------------------------------------------#
    ##Entry Boxes used in popup
    e1 = Entry(master,width=50)
    e2 = Entry(master,width=50)
    e3 = Entry(master,width=50)
    e4 = Entry(master,width=50)
    
    e1.grid(row=0, column=1)# Too place things neatly
    e2.grid(row=1, column=1)
    
    Label(master,text="If multiple parents seperate with \",\"",font="Myriad").grid(row=2,columnspan=4)
    
    e3.grid(row = 3,column=1)
    e4.grid(row=4,column=1)
    
    if data.addFlag==True:# add flag is if user wants to add child for selected 
        e2.insert(0,data.nodeClicked)# Automatically inserts parent name in e2 
    else:
        e2.delete(0,"end")
    entries = [e1,e2,e3,e4]
    
    
    
    
    
    ## Function within addCommand()
    ## this function is related to the add command popup
    ## it reads what the user has entered and inserts into the database 
    
    def save():# to run the save command on "save" button
        metaData=[]
        name = e1.get()
        if data.addFlag==False:
            data.nodeClicked=""
            parent = e2.get()
            parent = parent.split(",")# to consider if more than 1 parents are added 
            
        else:# if add child for selected node
            parent = [data.nodeClicked]
        description = e3.get()
        links = e4.get().split(",")# if more than one links entered. Spliting on "," to know when a           #       link ends
    
        for link in links:
            metaData.append([link,"",""])# [link,LinkName,Date]. Initally linkname and date are blank, gets updated when data is scraped 
            
        if len(parent)==1:# only one parent 
            if(getId(conn(),parent[0])==None):
                # Error checking 
                error =Tk()
                Message(error,text="Please select a valid Parent name",font="Myriad 15").grid(row=0,columnspan=3)
                Button(error,text="OK",font="Myriad 14",command=error.destroy).grid(row=1,column=1)
            else:
                # these functions are in databaseFunctions.py
                addToNodes(conn(),name,description,metaData)#  Adding data to nodes table 
                addToParent(conn(),name,parent[0])
                
                #this is found in updateTree.py
                updateTree(frame,data.tree,name,description,links,parent[0])
                
                #found in UI.py
                updateLinks(data)
                
                parent=[]
                
                # destory popUp once command executed 
                master.destroy()
                
                # flag is set to True to indicate data needs to be scraped 
                data.updateFlag = True 
                # name inidcates for which node data has to be scraped 
                data.updateNodeName = name
        else:
            # more than 1 parent 
            
            # this is in databaseFunctions.py
            addToNodes(conn(),name,description,metaData)#  Adding data to nodes table 
            flag = False # to show popup only once since in a for loop 
            for p in parent:#if more than 1 parent 
                if(getId(conn(),p)==None):
                    if flag==False:
                        # error checking 
                        error =Tk()
                        Message(error,text="One or more of the parent names entered were invalid",font="Myriad 15").grid(row=0,columnspan=3)
                        Button(error,text="OK",font="Myriad 14",command=error.destroy).grid(row=1,column=1)
                        flag = True 
                
                else:
                    #No ERRORS
                    # Adding data to nodes table 
                    
                    #databaseFunctions.py
                    addToParent(conn(),name,p)
                    
                    #treeFunctions.py
                    updateTree(frame,data.tree,name,description,links,p)
             
            # updateFlag to indicate data needs to be scraped
            data.updateFlag = True 
            #updateNodeName is the node name whose links need to be scraped 
            data.updateNodeName = name
            
            
            #Destroy popup
            master.destroy()
            parent=[]
                
    Button(master, text='Save', command=save).grid(row=6, column=1, sticky=W, pady=4)
    







## If user wants to update a Node, when update button is clicked 

def updateCommand(data):
    
    # master is a new tk window, popup 
    master = Tk()
    
    # Labels Used
    Label(master, text="Enter Node Name").grid(row=0)
    Label(master, text="Node Name").grid(row=3)
    Label(master, text="Description").grid(row=4)
    Label(master, text="Links").grid(row=5)
    
    
    # Entry boxes used 
    e1 = Entry(master)
    e2 = Entry(master)
    e3 = Entry(master)
    e4 = Entry(master,width=80)
  
    e1.grid(row=0, column=1)
    e2.grid(row=3,column=1)
    e3.grid(row=4,column=1)
    e4.grid(row=5,column=1,columnspan=3)
    entryLink = Entry(master,width=80)
    entries = [e4]

   

    ## When the user enters a node name that they want to update, this retireves data about that ######node 
    def retrieve():
        numLinks=0
        name = e1.get()
        elements = readRow(conn(),name)
        if elements==None:
            error =Tk()
            Message(error,text="Invalid Node Name",font="Myriad 15").grid(row=0,columnspan=3)
            Button(error,text="OK",font="Myriad 14",command=error.destroy).grid(row=1,column=1)
        else:
            description = elements[2]
            links,metaData = readLinks(conn(),name)
            
            # insert enters data from db into entry boxes 
            e2.insert(0,name)
            e3.insert(0,description)
            # if the existing node has no links 
            if links==None:
                print("None")
                e4.insert(0,"")
                
            # if node has links 
            else:
            
                if len(links)==1:
                    e4.insert(0,links)
                elif len(links)==0:
                    e4.insert(0,"")
                else:
                    e4.insert(0,links[0])
                    numLinks=len(links)
                    
                    # to create and entry box for each link of that node 
                    for x in range (1,numLinks):
                        entry = Entry(master,width=80)
                        entry.grid(row=x+5,column=1,columnspan=3)
                        entry.insert(0,links[x])
                        entries.append(entry)
            
            # this is the entry box for entering new link/links             
            entryLink.grid(row=numLinks+6,column=1,columnspan=3)
            entries.append(entryLink)
            Label(master,text="Enter new Link/Links").grid(row=numLinks+6)
            Message(master, text="If you want to enter more than one link seperate them with a \",\"",font="Myriad 10").grid(row=numLinks+7)
        
            
          
            ## after user clicks on save this inserts updated data in the db
            def saveChanges():
                newName = e2.get()
                description=e3.get()
                links = []
                if e4.get()=="":
                    print("No links existed before")
                    links.append(entryLink.get())
                else:
                    for entry in entries:
                        if entry.get().replace(" ", "")!= "":
                            links.append(entry.get())
                        else:
                            links.append("")
                    
                        
            
                num = len(metaData)
                
                
                
                # if any existing links updated 
                for x in range(num):
                    metaData[x][0] = links[x]
                
                
                # for new links entered by user 
                remaining_links = links[num:] #creates list of new links to be added 
                remaining_links = (remaining_links[0].split(","))
                for link in remaining_links:# if any new links added 
                    # if it is a new link, then the title and date columns are blank="",""
                    metaData.append([link,"",""])
                
                
                # db function
                update(conn(),name,newName,description,metaData)
                
                #front end Tree function, to update tree 
                updateT(frame,data.tree,name,newName,description,links)
                
                # db function
                data.links,data.newMeta = readLinks(conn(),newName)
            
                
                
                # function in UI.py
                updateLinks(data)
                # destroy the popup
                master.destroy()
                
                
                # is to deal with the links for this node have to be updated
                # use webscraper for links of this node 
                data.updateNodeName = newName
                # flag = True, means the scraper function should run, check Timer Fired below in this file 
                data.updateFlag = True 
                
            
                
        
                
                
            
            Button(master, text='Save Changes', command=saveChanges).grid(row=numLinks+7, column=1, sticky=W, pady=4)
        
        
    
    Button(master, text='Submit', command=retrieve).grid(row=0, column=2, sticky=W, pady=4)
    
    






## IF user wants to add link/links for selected node
## Reads old links, adds new links to old links
## flag to scrape new link is set true 
## CALLED When ser clicks add link button
def addLink(data,event):
    
    #read entry box
    links = data.linkEntry.get().split(",")  
    
    # the node clicked on the front end   
    name = data.nodeClicked 
    
    # this is used for scraping the link for this node, check TimerFired below
    data.updateNodeName  = name 
    
    # db function   
    data.oldLinks = addLinks(conn(),name,links)
    
    # clear the link entry box after user clicks submit
    data.linkEntry.delete(0, 'end')
    
    # db function, gets links and metaData of links for a node 
    data.links,data.newMeta = readLinks(conn(),data.nodeClicked)
    
    # this updates the links based on users entry 
    updateLinks(data)
    
    
    
   
    
    
    
### Function to update selected Node 
def updateSelection(data):
    
    # retrive data based on nodeclicked 
    def retrieve():
        numLinks=0
        elements = readRow(conn(),name)
        description = elements[2]
        
        #db function
        links,metaData = readLinks(conn(),name)
       
        e2.insert(0,name)
        e3.insert(0,description)
        if links==[] or links=="":
            print("None")
            e4.insert(0,"")
        else:
          
            if len(links)==1:
           
                e4.insert(0,links)
            else:
                e4.insert(0,links[0])
                numLinks=len(links)
             
                for x in range (1,numLinks):
                    
                    entry = Entry(master,width=80)
                    entry.grid(row=x+5,column=1,columnspan=3)
                    entry.insert(0,links[x])
                    entries.append(entry)
        entryLink.grid(row=numLinks+6,column=1,columnspan=3)
        
        entries.append(entryLink)
        
        Label(master,text="Enter new Link/Links").grid(row=numLinks+6)
        Message(master, text="If you want to enter more than one link seperate them with a \",\"",font="Myriad 10").grid(row=numLinks+7)
       
        
             
        
        ## Once user has entered updated data and clicked save 
        ## saves changes in the db 
        def saveChanges():
            
            # read entry fields 
            newName = e2.get()
            description=e3.get()
            links = []
            
            
            # entries is a list of entry box widgets for links
            for entry in entries:
                    
                if entry.get().replace(" ", "")== "" and entry!=entryLink:
                    
                    links.append("")
                else:
                    
                    links.append(entry.get())
               
            num = len(metaData)
            print(num)
            # if any existing links updated 
            for x in range(num):
                if links[x]!="":
                    metaData[x][0] = links[x]
                else:
                    metaData[x][0] = ""
            
            
            print("Meta")
            print(metaData)
            # for new link/links added 
            if entryLink.get().replace(" ","")!="":# only if something is entered into "ENTER LINKS"
                remaining_links = links[num:] #creates list of new links to be added 
                
                if remaining_links[0]!="":
                    remaining_links = (remaining_links[0].split(","))
                else:
                    
                    remaining_links = remaining_links[1].split(",")
                for link in remaining_links:# if any new links added 
                
                    #title and date fields are blank initially 
                    metaData.append([link,"","",])
            
            print(metaData)
            # update the db
            update(conn(),name,newName,description,metaData)
            
            #update the nodes tree 
            updateT(frame,data.tree,name,newName,description,links)
            
            # db function
            data.links,data.newMeta = readLinks(conn(),newName)
            
            # function in UI.py , look above 
            updateLinks(data)

            # destroy the popup
            master.destroy()
            
            
            # flag = True, means the scraper function should run, check Timer Fired below in 
            data.updateFlag = True 
            
            # is to deal with the links for this node have to be updated
            # use webscraper for links of this node 
            data.updateNodeName = newName
            
            
            
        Button(master, text='Save Changes', command=saveChanges).grid(row=numLinks+7, column=1, sticky=W, pady=4)
    name = data.nodeClicked
    
    # popup window 
    master = Tk()
    
    
    # labels used 
    Label(master, text="Node Name").grid(row=3)
    Label(master, text="Description").grid(row=4)
    Label(master, text="Links").grid(row=5)
   
   
    # entry boxes used 
    e2 = Entry(master)
    e3 = Entry(master)
    e4 = Entry(master,width=80)
  
    
    e2.grid(row=3,column=1)
    e3.grid(row=4,column=1)
    e4.grid(row=5,column=1,columnspan=3)
    entryLink = Entry(master,width=80)
    entries = [e4]
    retrieve()



def getTree(data):
    return d.treeBox



## Creates the hoverboxes used 
## uses the hoverBoxes.py file 

def createHoverBox(iid,data):
    if data.twFlag ==  True:
        data.tw.destroy()
    else:
        data.twFlag = False 
    
    x = y = 0
    x += root.winfo_pointerx() + 25
    y += root.winfo_pointery() + 20
    data.tw = tk.Toplevel(data.treeBox)
    data.tw.wm_overrideredirect(True)
    data.twFlag = True 

    data.tw.wm_geometry("+%d+%d" % (x, y))
    label = tk.Label(data.tw, text=iid, justify='left',
            background='yellow', relief='solid', borderwidth=1,
            font=("Myriad", "12", "normal"))
    label.pack(ipadx=1)
    
    
            



## this is to display data for links
def mycallback(event,data,arg):

    # idnetify link in treebox
    iid = data.treeBox.identify_row(event.y)
    
    if iid!="":
        
        if iid != data.last_focus:
            link=[]
            linksList = data.newMeta
            for element in linksList:
                if element[1]!= "":
                    if element[1]==iid:
                        link = element[0]
                else:
                    if element[0]==iid:
                        link = element[0]
           
            createHoverBox(link,data)
            
            if data.last_focus:
                
                
                data.treeBox.item(data.last_focus, tags=[])
                
            data.treeBox.item(iid, tags=['focus'])
            data.last_focus = iid
    else:
        data.last_focus=None
        if type(data.tw)!= str:
            data.tw.destroy()
    
    



## Hover boxes used to diplay nodeName in data.tree 
def mycallback_Tree(event,data,arg):
    iid = data.tree.identify_row(event.y)
    if iid!="":
        if iid != data.last_focus_tree:
            
            
            createHoverBox(iid,data)
            
            if data.last_focus_tree:
                data.tree.item(data.last_focus_tree, tags=[])
                
            data.tree.item(iid, tags=['focus'])
            data.last_focus_tree= iid
    else:
        data.last_focus_tree=None
        if type(data.tw)!= str:
            data.tw.destroy()
    
    
    


## Hover box used in Search popup 
def mycallback_tree1(event,data,arg):
    iid = data.tree1.identify_row(event.y)
    if iid!="":
        if iid != data.last_focus_tree1:
            
            createHoverBox(iid,data)
            
            if data.last_focus_tree1:
                data.tree1.item(data.last_focus_tree1, tags=[])
                
            data.tree1.item(iid, tags=['focus'])
            data.last_focus_tree1= iid
    else:
        data.last_focus_tree1=None
        if type(data.tw)!= str:
            data.tw.destroy()
    
    
    

## when the user clicks on a link in data.treeBox it should open the webbrowser 
def immediately(event,data):
    
    if(event.widget==data.listBox):
        index = data.listBox.curselection()
        name = data.listBox.get(index)
        list = data.linksDict.items()
        for element in list:
            if element[1]==name:
                data.htmlLink = element[0]
                webbrowser.open(data.htmlLink, new=2)
                
                
                print(data.htmlLink)



@cached(cache)


## anytime a mouse is pressed by the user 
def homeScreenMousePressed(event, data):
    
    
    
    ## Add Node button clicked 
    if event.widget==data.addButton:
        data.addFlag=False
        
        # this is in UI.py
        addCommand(data)
    
    
    
## If user clicks on a link in the tree 

    if event.widget == data.treeBox:
        name=""
        
        # identify the link
        item = data.treeBox.identify("item", event.x, event.y)
        
        # column #2 is the attachments, if the user clicks on that it will not work 
        if (data.treeBox.identify_column(event.x)=="#2"):#IF user wants to see attachments 
            link = None 
            
            # idenitfy the link 
            name = (data.treeBox.item(item)["text"])
            
            
            linksList = data.newMeta
            for element in linksList:
                if element[1]==name:
                    link = element[0]
            
            
            # this is the relevant attachments data for the link
            # IMP
            # EXPLANATION FOR THE USE OF .split(", SPLITTER,") IS IN databaseFunctions.py
            attachmentsData = getAttachments(conn(),link,data.nodeClicked).split(", SPLITTER,")
            
            # use this if need to debug 
            print(attachmentsData)
            
            
            if attachmentsData == ['None']:
                print("NO")
            
            
            
            filesDict,tableData,imgsDict = attachmentsData[0].strip(","),attachmentsData[1].strip(","),attachmentsData[2].strip(",")
            
            
        
            # incase the json arrray is malformed 
            filesDict = filesDict.replace("[","")
            
            # the attachments.py file adds satabase URL
            
            # this is not really used 
        
            filesDict = filesDict.replace("https://","") 
            filesDict = filesDict.replace("http://","")
            
            tableData = tableData.strip()
            
            # makes a list of all table headers for the link 
            [tableData] = [tableData.strip("[]").split(",")]
            
            # use this to debug
            #print(tableData)
            
            
            # for images and their links 
            imgsDict = imgsDict.replace("https://","") 
            imgsDict = imgsDict.replace("http://","")
            imgsDict = imgsDict.strip("]")
            imgsDict= imgsDict.strip()
            
            #print(imgsDict)
            
            # this creates a dictionary of imagelink : image link or imagelink:imagelink
            # this is done because the dict read form db is a sring
            imgsDict = dict([item.split(":") for item in imgsDict.strip('{}').split(",")])
        
            
            # if filesDict exists in db 
            if filesDict!="{}":
                
                # this  creates the dictionary of attachment name: attachment 
                filesDict = dict([item.split(":") for item in filesDict.strip('{}').split(",")])
            else:
            
                print("BLANK")
                filesDict = dict()
            
            
            
            # make the popup window 
            master = Tk()
            
            # this is seen in attahments.py file 
            run2(master,filesDict,imgsDict,tableData,width=300, height=200)
        
        
        # is user clicks on links and not on attachment column 
        else:
            
            # identify the link name and match it to a link and open webbrowser 
            name = (data.treeBox.item(item)["text"])
            if name != "":
                linksList = data.newMeta
                
                for element in linksList:
                    if element[1]!="":
                        if element[1]==name:
                            data.htmlLink = element[0]
                            webbrowser.open(data.htmlLink, new=2)
                    else:
                        if element[0]==name:
                            data.htmlLink = element[0]
                            webbrowser.open(data.htmlLink, new=2)
                            
                        
            

           
    
## when user clicks search button
## read search, read link and nodes from db, check what matches, create lists of matches and ###display in popup
    if event.widget == data.searchButton:
        nameslist=[]
        linkslist=[]
        
        # db function
        links,names,linksAndText = getLinks(conn())
        
        
        searchQuery = data.searchEntry.get().split()
        
       
        # if more than one words entered into the query 
        for text in searchQuery:
            
            
            # format for regex 
            query=".*"+text
            print(query)
            
            # re.compile is a regex function
            r = re.compile(query,re.IGNORECASE)
            
            # makes a list of matching links to query 
            linkslist+=  list(filter(r.match, links)) # Read Note
            
            
            # use this print to debug
            #print(linkslist)
            
            
            if linkslist==[]:
                numberOfLinks=0
            else:
                numberOfLinks = len(linkslist)
            
            
            # checks for mathcing node names to search query 
            r = re.compile(query,re.IGNORECASE)
            nameslist += list(filter(r.match, names)) 
        
        
        # set is used to remove duplicates 
        nameslist = list(set(nameslist))
        linkslist = list(set(linkslist))
        
        #print(linkslist,nameslist)
        
        dict1= linksAndText
        
        # make a popup
        master = Tk()
        
        # called in searchpopUp.py
        run1(master,linkslist,dict1,numberOfLinks)
        
        
        
        # this is the tree made in the search popUp
        # has relevant node names to search query 
        data.tree1 = ttk.Treeview(master,height=10,columns=("A","B"))
        data.tree1.grid(row=1,column=0,columnspan = 3,rowspan=2)
        data.tree1.heading("#0", text="Nodes with similar name")
        data.tree1.heading("A", text="")
        data.tree1.heading("B", text="Node Path with similar name")
        data.tree1.column("A",minwidth=0,width=0, stretch=NO)
        data.tree1.column("B",minwidth=400,width=600, stretch=NO)
        data.tree1.tag_configure('focus', background='yellow')
        
        data.tree1.bind("<Motion>",lambda event, arg=data: mycallback_tree1(event,data,arg))
        data.last_focus_tree1=None
        
        for name in nameslist:
            
            
           # print(getPath(conn(),name))
            #recursive function in db functionss
            path = getPath(conn(),name)
            data.tree1.insert("",2,name,text =name,values=("",path))
        
        data.searchEntry.delete(0,'end')
        
        data.linkEntry.delete(0, 'end')
        
        
    
        
        
    
## If user wants to add a child for selected node 
    if event.widget==data.addSelectedButton:
        
        
        # flag is useful for addCommand(data)
        # funciton reads nodeclicked as parent name 
        data.addFlag=True 
        addCommand(data)
        

## if user wants to update a selected node 
    if event.widget==data.updateSelectedButton:
        updateSelection(data)
        

## update a node 
## user enters node name and then updates 
    if event.widget==data.updateButton:
        
        updateCommand(data) 
        if data.links!=None:
            numberOfLinks = len(data.links)
        else:
            numberOfLinks = 0       # to prevent error caused when len(None)
        
        updateLinks(data)
        
## add links for selected node 
    if(event.widget==data.addLinkButton):
        
        
        # user should have selected a node 
        if data.nodeClicked=="":
            error =Tk()
            Message(error,text="Please select a node",font="Myriad 15").grid(row=0,columnspan=3)
            Button(error,text="OK",font="Myriad 14",command=error.destroy).grid(row=1,column=1)
        elif data.linkEntry.get().replace(" ", "")=="":
            error =Tk()
            Message(error,text="Please enter a link/links",font="Myriad 15").grid(row=0,columnspan=3)
            Button(error,text="OK",font="Myriad 14",command=error.destroy).grid(row=1,column=1)
        
        else:
            # function in UI.py
            addLink(data,event)
            
            # seen in TimerFired() below 
            # flag indicates scraping needs to be done 
            # scraping needs to be done for node clicked 
            data.updateNodeName = data.nodeClicked
            data.updateLinkFlag = True 
            
            
    
    # if user clciks the nodes tree 
    if(event.widget==data.tree):
        

        data.nodeClicked=""
        
        item = data.tree.identify("item", event.x, event.y)
        data.nodeClicked = (data.tree.item(item)["text"])
        if data.nodeClicked != "":
            data.last_focus=None
            data.nodeClicked = data.nodeClicked.strip()
            
            # db function
            data.links,data.newMeta = readLinks(conn(),data.nodeClicked)
            
            # dict of {link name: link}
            data.linksDict = convertLinks(data.links)
            
            
            if data.links!=None:
                numberOfLinks = len(data.links)
            else:
                numberOfLinks = 0       # to prevent error caused when len(None)
            numberOfLinks=(30)
            

            updateLinks(data)
            


## open webbrowser 
def callback(event,link):
    webbrowser.open_new(r)
    
    
## for future extensibility 
def homeScreenKeyPressed(event, data):
    
    pass
    
    
## called every 1000 milliseconds, 1 second 
def homeScreenTimerFired(data):
    data.updateServiceTime +=1
    
    if data.updateServiceTime>= 180:# 3600 seconds in an hour 
        print("HI")
        data.updateServiceTime=0
    
    
    
    ## this flag is for updating all links in  NODE 
    if data.updateFlag==True:
        print("SCRAPING")
        links,meta = readLinks(conn(),data.updateNodeName)
        newMeta=[[]]
        
        # SCRAPER.PY FUNCTION
        newMeta = convert(links)
        
        # db fucntion 
        insertMetadata(conn(),data.updateNodeName,newMeta)
        data.links,data.newMeta = readLinks(conn(),data.updateNodeName)
        
        #UI.py function for front end 
        updateLinks(data)
        print("INSERTED")
        
        # set flag to false again 
        data.updateFlag = False
        data.updateNodeName = ""
    
    
    ## this flag is to update only new links added, used if link added through addLink button 
    if data.updateLinkFlag == True:
        print("LINK")
        links,meta = readLinks(conn(),data.updateNodeName)
        
        newLinks= list(set(links)-set(data.oldLinks))
        for link in newLinks:
            pos = meta.index([link,"","","[]"])
            #print(meta[pos],pos)
            
            newMeta = convert([link])
            #print(newMeta)
            [meta[pos]] = newMeta
            
        #print(meta)
        
        insertMetadata(conn(),data.updateNodeName,meta)
        data.links,data.newMeta = readLinks(conn(),data.updateNodeName)
        updateLinks(data)
        data.updateLinkFlag = False 
        data.updateNodeName=""
        
        
        
        
        
def homeScreenRedrawAll(canvas, data):
    #threading.Timer(10, updateData(conn(),data))
    pass 
    
    

####################################
# use the run function as-is
####################################

def run(width=700, height=700):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds # 1000 miliseconds is 1 second 
    init(data,frame)
    
    
    # create the root and the canvas

    screen_width = int(root.winfo_screenwidth())
    screen_height = int(root.winfo_screenheight())
    #quitButton = Button(root,text="See WikiLinks For this Node",command=print("hi"))

        # placing the button on my window
    #quitButton.pack(ipadx=0, ipady=0)
    
    
    
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    
    # and launch the app
    
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()
