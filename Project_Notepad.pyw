# Author : Patel Riyank 
# Date : 27 Dec 2020 

#################### NOTEPAD - GUI ############################

from tkinter import *
import tkinter.messagebox as tmsg
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os



def newFile(event=None):
    '''
    This function make the new file in notepad. 
    It just clear the whole text area means delete the whole text from the text area  if some another file was open.
    And set the title as Untitled.
    '''
    global file
    root.title("Untitled - Notepad")
    file = None
    TextArea.delete(1.0,END)

def openFile(event=None):
    '''
    This function can open the existing file store in the pc. 
    '''
    global file
    file = askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Document","*.txt")]) # this opens the prompt to select the existing file from the local storage.

    if file == "":
        file = None
    else:
        TextArea.delete(1.0,END)
        f = open(file, "r")
        TextArea.insert(1.0,f.read())            # inserting the data of the selected file in the text area.
        root.title(os.path.basename(file.replace(".txt","")) + " - Notepad")
        f.close()
        showline()

def saveFile(event=None):
    '''
    This function saves the file in local storage.
    '''
    global file
    global savedFile
    if file == None:        # save as a newfile
        file = asksaveasfilename(initialfile = "Untitled.txt",defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Document","*.txt")]) # this open the prompt to save the file
        if file == "":
            file = None
        else:
            f = open(file,"w")
            f.write(TextArea.get(1.0,END))
            f.close()
            savedFile = True
            root.title(os.path.basename(file.replace(".txt","")) + " - Notepad")

    else:       # save the existing file
        
        f = open(file,"w")
        f.write(TextArea.get(1.0,END))
        f.close()
        savedFile = True

def cut(event=None):
    '''
    The selected area is cut and copy to the clipboard.
    '''
    TextArea.event_generate(("<<Cut>>"))

def copy(event=None):
    '''
    To copy the selected area.
    '''
    TextArea.event_generate(("<<Copy>>"))

def paste(event=None):
    '''
    To paste the content of the clipboard
    '''
    TextArea.event_generate(("<<Paste>>"))

def about():
    tmsg.showinfo("Notepad","Notepad By Patel Riyank")   # opens one dialogbox with the specific information here it is "Notepad By Patel Riyank"

def showline(event=None):
    '''
    It shows the position of the pointer(blinker) of the textarea.
    '''
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
    
    # Creating a menubar
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

    # Defining shortcuts.
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
    root.mainloop()  # this is the mainloop which can run continously to show the all above Content.
