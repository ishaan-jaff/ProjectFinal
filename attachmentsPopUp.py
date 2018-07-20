

## This is the file creating the popup when user clicks on attcahments 
try:
    # for Python3
    from tkinter import*
except ImportError:
    # for Python2
    import Tkinter as tk
    
from list import*
import webbrowser




#########        Functions

## This is when the user clicks on an element in the popup, the web link should open if it is an image or a file 
def immediately(event,data):
    
    # 2 modes
    # in Files mode, there are attachments that can be seen 
    # this mode has attachments and images 
    if data.mode== "Files":
        
        
        # lb is for attachments 
        if(event.widget==data.lb):
            index = data.lb.curselection()
            name = data.lb.get(index)
            list = data.files.items()
            
            for element in list:
                print(element[0],name)
                if element[0].strip()==name:
                    data.htmlLink = "https://spaces.telenav.com:8443"+(element[1].strip())
                    print(data.htmlLink)
                    webbrowser.open(data.htmlLink, new=2)
                    
          
                    
        # lb1 is for images 
        if event.widget==data.lb1:
            index = data.lb1.curselection()
            name = data.lb1.get(index)
            list = data.imgsDict.items()
            #print(list)
            for element in list:
                if element[0].strip()==name:
                    # this is the database url :
                    #https://spaces.telenav.com:8443
                    
                    data.htmlLink = "https://spaces.telenav.com:8443"+(element[1].strip())
                    print(data.htmlLink)
                    webbrowser.open(data.htmlLink, new=2)
    
    
    
    # in this mode there are no files, images and tableheaders are shown 
    if data.mode=="NoFiles":
        
        # lb is used for images in this mode 
        if event.widget==data.lb:
            index = data.lb.curselection()
            name = data.lb.get(index)
            list = data.imgsDict.items()
           
            for element in list:
                if element[0].strip()==name:
                    data.htmlLink = "https://spaces.telenav.com:8443"+(element[1].strip())
                    print(data.htmlLink)
                    webbrowser.open(data.htmlLink, new=2)
            
        

## variables used
def init(data,master,filesDict,imgsDict,tableData):
    data.lb = Listbox(master,height=20,font="Myriad",width=45)
    
    data.files = filesDict
    data.imgsDict = imgsDict
    data.tableHeaders = tableData
    
    data.lb.grid(row=1,column=0,rowspan=3)
    data.lb1 = Listbox(master,height=20,font="Myriad",width=45)
    data.lb1.grid(row = 1,column = 1)
    data.htmlLink=""


   
    data.fileNames = list(data.files.keys())
    data.imgNames = list(data.imgsDict.keys())
    
    
    
    
    ## THis has two modes based on if attachments/files exist or not 
    if data.fileNames!=[]:
        data.mode = "Files"
        data.label1 = Label(master,text = "Attachment Files",font = ("Myriad",18))
        data.label2 = Label(master,text = "Images",font = ("Myriad",18))
       
        fillAttachments(data.fileNames,data.lb,30)
        fillImages(data.imgNames,data.lb1,30)
    else:
        data.mode= "NoFiles"
        data.label1 = Label(master,text = "Images",font = ("Myriad",18))
        data.label2 = Label(master,text = "Table Headers on this link",font = ("Myriad",18))
        fillTableData(data.tableHeaders,data.lb1,30)
        fillImages(data.imgNames,data.lb,30)
    data.label1.grid(row =0,column=0)
    data.label2.grid(row=0,column=1)
    
def mousePressed(event, data):
    if event.widget==(data.lb) or event.widget==(data.lb1):
        data.lb.bind('<<ListboxSelect>>', immediately(event,data))
      
def redrawAll(canvas, data):
    pass
    
    
## this makes the popup
def run2(master,filesDict,imgsDict,tableData,width=300, height=200):

    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    
   
    
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data,master,filesDict,imgsDict,tableData)
    # create the root and the canvas

    screen_width = int(master.winfo_screenwidth())
    screen_height = int(master.winfo_screenheight())
    
    
    
    canvas = Canvas(master, width=data.width, height=data.height)
    canvas.grid()
    # set up events
    master.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    master.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    #timerFiredWrapper(canvas, data)
    
    # and launch the app
    
    #master.mainloop()  # blocks until window is closed
    print("bye!")

