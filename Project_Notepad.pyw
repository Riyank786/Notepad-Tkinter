# Author : Patel Riyank 
# location : Mars 
# Date : 27 Dec 2020 

#################### NOTEPAD - GUI ############################

from tkinter import *
import tkinter.messagebox as tmsg
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os



def newFile(event=None):
    global file
    root.title("Untitled - Notepad")
    file = None
    TextArea.delete(1.0,END)

def openFile(event=None):
    global file
    file = askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Document","*.txt")])

    if file == "":
        file = None
    else:
        TextArea.delete(1.0,END)
        f = open(file, "r")
        TextArea.insert(1.0,f.read())
        root.title(os.path.basename(file.replace(".txt","")) + " - Notepad")
        f.close()
        showline()

def saveFile(event=None):
    global file
    global savedFile
    if file == None:
        file = asksaveasfilename(initialfile = "Untitled.txt",defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Document","*.txt")])
        if file == "":
            file = None
        else:
            # save as a newfile
            f = open(file,"w")
            f.write(TextArea.get(1.0,END))
            f.close()
            savedFile = True
            root.title(os.path.basename(file.replace(".txt","")) + " - Notepad")

    else:
        # save the newfile
        f = open(file,"w")
        f.write(TextArea.get(1.0,END))
        f.close()
        savedFile = True

def cut(event=None):
    TextArea.event_generate(("<<Cut>>"))

def copy(event=None):
    TextArea.event_generate(("<<Copy>>"))

def paste(event=None):
    TextArea.event_generate(("<<Paste>>"))

def about():
    tmsg.showinfo("Notepad","Notepad By Patel Riyank")

def showline(event=None):
    line = int(TextArea.index(INSERT).split(".")[0])
    column = int(TextArea.index(INSERT).split(".")[1])
    showLC.config(text=f"Ln  {line}, Col  {column+1}")

def changeFormat():
    if wordwrap.get() == True:
        TextArea.config(wrap=WORD)
    else :
        TextArea.config(wrap=NONE)

def hideStatus():
    if statusvar.get() == True:
        footer.pack(side=BOTTOM,fill=X)
    else :
        footer.pack_forget()

def doSomething():
    if savedFile:
        root.destroy()
    else:
        ans = tmsg.askyesnocancel("Notepad","Do you want to save changes to Untitled?")
        if ans == True:
            saveFile()
            root.destroy()
        elif ans == False:
            root.destroy()


def key_press(event):   
    global savedFile
    savedFile=False

if __name__ == "__main__": 
    root = Tk()
    root.title("Untitled - Notepad")
    root.geometry("644x534")

    savedFile = True
    # Let's create a menubar
    MenuBar = Menu(root)

    ##### FILE MENU START #####
    FileMenu = Menu(MenuBar, tearoff = 0)  
    FileMenu.add_command(label="New             Ctrl+N", command = newFile) 
    FileMenu.add_command(label="Open...        Ctrl+O", command= openFile)
    FileMenu.add_command(label="Save             Ctrl+S", command = saveFile)
    FileMenu.add_separator()
    FileMenu.add_command(label="Exit              Alt+F4", command = root.destroy)
    MenuBar.add_cascade(label="File", menu=FileMenu)
    ##### FILE MENU END #####

    ##### EDIT MENU START #####
    EditMenu = Menu(MenuBar, tearoff = 0)
    EditMenu.add_command(label="Cut                Ctrl+X", command=cut)
    EditMenu.add_command(label="Copy             Ctrl+C", command=copy)
    EditMenu.add_command(label="Paste             Ctrl+V", command=paste)
    MenuBar.add_cascade(label="Edit", menu=EditMenu)
    ##### EDIT MENU END #####

    ##### FORMAT MENU START #####
    wordwrap = BooleanVar()
    statusvar = BooleanVar()
    statusvar.set(True)
    FormatMenu = Menu(MenuBar, tearoff = 0)
    FormatMenu.add_checkbutton(label="Word Wrap",variable=wordwrap,command=changeFormat)
    FormatMenu.add_checkbutton(label="Status Bar",variable=statusvar,command=hideStatus)
    Fontmenu = Menu(FormatMenu,tearoff = 0) 
    MenuBar.add_cascade(label="Format", menu=FormatMenu)
    ##### FORMAT MENU END #####

    ##### HELP MENU START #####
    HelpMenu = Menu(MenuBar, tearoff=0)
    HelpMenu.add_command(label="About Notepad", command=about)
    MenuBar.add_cascade(label="Help",menu=HelpMenu)
    ##### HELP MENU END #####

    root.config(menu = MenuBar)

    f = Frame(root,borderwidth=2,bg="white")
    f.pack(fill=BOTH,expand = True)

    frame1 = Frame(f, borderwidth=2,bg="white")
    frame2 = Frame(f, borderwidth=2,bg="white")
    frame3 = Frame(f, borderwidth=2,bg="white")

    frame1.grid(column=0, row=0, sticky="nsew") 
    frame2.grid(column=1, row=0, sticky="nsew")
    frame3.grid(column=0, row=1, sticky="nsew", columnspan = 2)

    Grid.columnconfigure(f,0,weight=1)
    Grid.columnconfigure(f,1,weight=0)
    Grid.rowconfigure(f,0,weight=1)
    Grid.rowconfigure(f,1,weight=0)

    # Add text Area
    TextArea = Text(frame1, font="Consolas 20", wrap=NONE)
    TextArea.pack(expand = True ,fill=BOTH)
    TextArea.focus()
    file = None
  
    # Adding Scrollbar
    ScrollY = Scrollbar(frame2)
    ScrollY.pack(side=RIGHT,fill=Y)
    ScrollY.config(command =TextArea.yview)

    ScrollX = Scrollbar(frame3, orient="horizontal",cursor="arrow")
    ScrollX.pack(side=TOP,fill=X)
    ScrollX.config(command =TextArea.xview)

    TextArea.config(yscrollcommand=ScrollY.set,xscrollcommand=ScrollX.set)


    # foooter 
    footer = Frame(frame3,relief=GROOVE,bg="white")
    footer.pack(side=BOTTOM,fill=X)
    Label(footer,text="Created By Riyank Patel",padx=10,relief=RAISED).pack(side=RIGHT)
    showLC=Label(footer,text="Ln  1, Col  1",padx=30,relief=RAISED)
    showLC.pack(side=RIGHT)  

    root.bind("<Control-s>",saveFile)
    root.bind("<Control-o>",openFile)
    root.bind("<Control-n>",newFile)
    root.bind("<Control-x>",cut)
    root.bind("<Control-c>",copy)
    root.bind("<Control-p>",paste)
    root.bind("<Control-S>",saveFile)
    root.bind("<Control-O>",openFile)
    root.bind("<Control-N>",newFile)
    root.bind("<Control-X>",cut)
    root.bind("<Control-C>",copy)
    root.bind("<Control-P>",paste)
    root.bind('<Key>', key_press)
    TextArea.bind("<KeyRelease>",showline) 
    root.protocol('WM_DELETE_WINDOW', doSomething)
    root.mainloop()