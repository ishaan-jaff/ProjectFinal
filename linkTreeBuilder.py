from tkinter import *
from list import*
import webbrowser
def immediately(event,data):
    
    if(event.widget==data.lb):
        index = data.lb.curselection()
        name = data.lb.get(index)
        list = data.linksDict.items()
        print(index,name)
        for element in list:
            if element[0]==name:
                data.htmlLink = element[1]
                webbrowser.open(data.htmlLink, new=2)
                
                
                print(data.htmlLink)

def init(data,master,filesDict,imgsDict,tableData):
    data.lb = Listbox(master,height=20,font="Myriad",width=45)
    data.files = filesDict
    data.imgsDict = imgsDict
    data.tableH = tableData
    
    data.lb.grid(row=0,column=2,rowspan=3)
    data.lb1 = Listbox(master,height=20,font="Myriad",width=45)
    data.lb1.grid(row = 0,column = 3)
    data.htmlLink=""
    
        
    fillList(data.frontEndLinks,data.lb,data.links,numberOfLinks)
def mousePressed(event, data):
    if event.widget==(data.lb):
       
        data.lb.bind('<<ListboxSelect>>', immediately(event,data))
      
def redrawAll(canvas, data):
    pass
    
    
    
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
    #quitButton = Button(master,text="See WikiLinks For this Node",command=print("hi"))

        # placing the button on my window
    #quitButton.pack(ipadx=0, ipady=0)
    
    
    
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

