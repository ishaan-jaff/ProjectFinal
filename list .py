from tkinter import *
import tkinter

root= Tk()
"""def immediately(e):
    #print (Lb1.curselection())
    print(Lb1.get(Lb1.curselection()))




Lb1 = Listbox(root,bg="gold2",bd=3,cursor="arrow",fg="RoyalBlue4",height=45,width=40,selectmode=SINGLE)
def makeList(list,Lb1):
    length = len(list)
    for x in range (length):
        Lb1.insert(x, list[x])
    Lb1.pack(side=RIGHT)
    Lb1.bind('<<ListboxSelect>>', immediately)
        
        

    root.mainloop()
makeList(["Python","Java","MySql"],Lb1)