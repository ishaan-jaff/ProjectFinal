try:
    # for Python3
    from tkinter import*
except ImportError:
    # for Python2
    import Tkinter as tk
    



## Fills list seen when "Search Button" is clicked on search popup
def fillList(list,Lb1,links,numberOfLinks):
    numberOfLinks = Lb1.size()
    Lb1.delete(0,numberOfLinks)
    if list!=None:
        length = len(list)
        for x in range (length):
            Lb1.insert(x,list[x])
    
    
## When user clicks on attachments, this fills the listbox for files/attachments
def fillAttachments(list,Lb1,numberOfLinks):
    numberOfLinks = Lb1.size()
    Lb1.delete(0,numberOfLinks)
    if list!=None:
        length = len(list)
        
        for x in range (length):
            Lb1.insert(x,list[x].strip())
        
## Fills the listbox for image links     
def fillImages(list,Lb1,numberOfLinks):
    numberOfLinks = Lb1.size()
    Lb1.delete(0,numberOfLinks)
    if list!=None:
        length = len(list)
        for x in range (length):
            Lb1.insert(x,list[x].strip())
        
## fils the list box for tableData
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
    