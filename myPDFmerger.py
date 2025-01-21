import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox 
import tkinterDnD  # Importing the tkinterDnD module
from pypdf import PdfWriter


# Remove all items in the listbox and reset the progress bar
def clearList():
    listbox.delete(0, listbox.size())

# Move selected item up in listbox
def moveup():
    posList = listbox.curselection()
    # exit if the list is empty
    if not posList:
        return
    for pos in posList:
    # skip if item is at the top
        if pos == 0:
            continue

        text = listbox.get(pos)
        listbox.delete(pos)
        listbox.insert(pos-1, text)
        listbox.selection_set(pos-1)


# Move selected item down in listbox
def movedown():
    posList = listbox.curselection()
    # exit if the list is empty
    if not posList:
        return

    for pos in posList:
    # skip if item is at the top
        if pos == listbox.size()-1:
            continue

        text = listbox.get(pos)
        listbox.delete(pos)
        listbox.insert(pos+1, text)
        listbox.selection_set(pos+1)

 # Remove selected item in listbox
def removeSelected():
    if not listbox.curselection():
        return
    listbox.delete(listbox.curselection())

# save as dialog
def saveAsDialog(): 
    files = [('PDF File', '*.pdf'),] 
    file = asksaveasfile(filetypes = files, defaultextension = files)
    return file.name

# Handle the files in listbox 1 by 1, and update the progress bar
def mergenow():
    if listbox.size() == 0:
        return

    get_content = listbox.get(0, listbox.size()) # get a tuple from listbox

    pdfs = [] # Array to store the pdf file list

    # Add the items into array in listbox 1 by 1
    for input_file in get_content:
        pdfs.append(input_file)

    #Pdf writer for merging the pdfs
    merger = PdfWriter()

    for pdf in pdfs:
        merger.append(pdf)

    file = saveAsDialog();

    merger.write(file)
    merger.close()

    messagebox.showinfo("File Merged", "File Merged")


# You have to use the tkinterDnD.Tk object for super easy initialization,
# and to be able to use the main window as a dnd widget
root = tkinterDnD.Tk()
root.title("myPDF Merger")

stringvar = tk.StringVar()
stringvar.set('Drag files here to merge +')


def drop(event):
    # This function is called, when stuff is dropped into a widget
#    stringvar.set(event.data)
    #print("DROP!")
    #print(event.data)
    
    if event.data[0] == '{':
        #print('has Space')
        x = event.data.split("} {")
        for item in x:
            item = item.replace('{', '')
            item = item.replace('}', '')
            file_ext = os.path.splitext(item.lower())[1]
            if file_ext == '.pdf':
                listbox.insert(0, item)
    else:
        #print("No Space")
        x = event.data.split()
        for item in x:
            file_ext = os.path.splitext(item.lower())[1]
            if file_ext == '.pdf':
                listbox.insert(0, item)


def drag_command(event):
    # This function is called at the start of the drag,
    # it returns the drag type, the content type, and the actual content
    print("DRAG!")
    return (tkinterDnD.COPY, "DND_Text", "Some nice dropped text!")







about_label_text = ('myPDF Merger v1.0 Build 25012101\n'
    'Author: Paul Chow\n'
    'Email: bong99@gmail.com\n'
    'License: MIT License\n\n'    
    'Github: https://github.com/Bong99/myPDF-merger'    
    )

def about():
    messagebox.showinfo("About", about_label_text) 

# UI Layout section start

# With DnD hook you just pass the command to the proper argument,
# and tkinterDnD will take care of the rest
# NOTE: You need a ttk widget to use these arguments

label_guide = tk.Label(root, text='\nDrag the PDF files to below area, then press "Merge" button to start merge.\n')
label_guide.pack()   

label_2 = ttk.Label(root, ondrop=drop, ondragstart=drag_command, textvar=stringvar, padding=50, relief="solid")
label_2.pack(fill="both", expand=True, padx=10, pady=10)

listbox = tk.Listbox(root)
listbox.pack(fill="both", expand=True, padx=10, pady=10)

button_frame = tk.Frame(root, width=400, height=50)
button_frame.pack()

buttonMoveUp = tk.Button(button_frame, text = "Move Up", command = moveup)
buttonMoveUp.pack(side='left', padx = 3, pady = 3)

buttonMoveDown = tk.Button(button_frame, text = "Move Down", command = movedown)
buttonMoveDown.pack(side='left',padx = 3, pady = 3)

buttonRemove = tk.Button(button_frame, text = "Remove Selected", command = removeSelected)
buttonRemove.pack(side='left',padx = 3, pady = 3)

button1 = tk.Button(button_frame, text = "Merge PDF now", command = mergenow)
button1.pack(side='left',padx = 3, pady = 3)

button2 = tk.Button(text = "Clear", command = clearList)
button2.pack(padx = 3, pady = 3)

button_about = tk.Button(text = "About...", command = about)
button_about.pack(padx = 3, pady = 3)

root.mainloop()