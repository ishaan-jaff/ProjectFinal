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

def init(data,master,linkslist,linksAndText,numberOfLinks):
    data.lb = Listbox(master,height=20,font="Myriad",width=45)
    data.links = linkslist
    data.linksDict = linksAndText
    data.frontEndLinks = list(linksAndText.keys())
    data.label1 = Label(master,text = "Node Names Matching Search Query",font = ("Myriad",18))
    data.label2 = Label(master,text = "Links Matching Search Query",font = ("Myriad",18))
    data.label1.grid(row =0,column=0)
    data.label2.grid(row=4,column=0)
    data.lb.grid(row=5,column=0,rowspan=3)
    data.htmlLink=""
    

    fillList(data.frontEndLinks,data.lb,data.links,numberOfLinks)
def mousePressed(event, data):
    if event.widget==(data.lb):
       
        data.lb.bind('<<ListboxSelect>>', immediately(event,data))
      
def redrawAll(canvas, data):
    pass
    


def run1(master,linkslist,dict1,numberOfLinks,width=600, height=400):

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
    init(data,master,linkslist,dict1,numberOfLinks)
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

