from tkinter import *
import tkinter
#from scraper import*

"""def immediately(e):
    print (Lb1.curselection())"""


def onEnter(e):
    pass
    #print("START")
def onLeave(e):
    pass
   # print("END")

def fillList(list,Lb1,links,numberOfLinks):
    numberOfLinks = Lb1.size()
    Lb1.delete(0,numberOfLinks)
    if list!=None:
        length = len(list)
        
        for x in range (length):
            
            
            Lb1.insert(x,list[x])
    
    #print(Lb1.curselection())

def fillAttachments(list,Lb1,numberOfLinks):
    numberOfLinks = Lb1.size()
    Lb1.delete(0,numberOfLinks)
    if list!=None:
        length = len(list)
        
        for x in range (length):
            Lb1.insert(x,list[x].strip())
        
        
def fillImages(list,Lb1,numberOfLinks):
    numberOfLinks = Lb1.size()
    Lb1.delete(0,numberOfLinks)
    if list!=None:
        length = len(list)
        for x in range (length):
            Lb1.insert(x,list[x].strip())
        
    
def fillTableData(list,Lb1,numberOfLinks):
    numberOfLinks = Lb1.size()
    Lb1.delete(0,numberOfLinks)
    if list!=None:
        length = len(list)
        for x in range (length):
            if list[x].replace(" ","")!="" and list[x]!="#":
                Lb1.insert(x,list[x].strip())
        
    
    

def makeList(Lb1):
    Lb1.pack()
    