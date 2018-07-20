import tkinter as tk
from tkinter import ttk

def OnDoubleClick(event):
    item = tree.selection()
    print('item:', item)
    print('event:', event)
    item = tree.selection()[0]

    print("you clicked on", tree.item(item,"text"))

root = tk.Tk()
tree = ttk.Treeview()
tree.pack()

for i in range(10):
    tree.insert("", "end", text="Item %s" % i)

#tree.bind("<Double-1>", OnDoubleClick) # double click
#tree.bind("<Button-1>", OnDoubleClick) # single click
tree.bind("<<TreeviewSelect>>", OnDoubleClick) # single click, without "index out of range" error

root.mainloop()