import tkinter as tk
from docx2pdf import convert

from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileReader
from pikepdf import Pdf


import os
from pathlib import Path





class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.path_value = tk.StringVar()
        #self.path_value.insert(0,"""C:\Users\test\Documents\Aufgaben Kombi\Name der Aufgabe""")
        self.path_l = tk.Label(self, text='Path to directory') 
        self.path_l.pack(side="top")
        
        self.path_e = tk.Entry(self, textvariable=self.path_value, width=100)
        self.path_e.pack(side="top")

        self.okay_b = tk.Button(self, text="Go", command=self.get_path_value)
        self.okay_b.pack(side="right")

        self.quit_b = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit_b.pack(side="right")

    def get_path_value(self):
        #print(self.path_value.get())
        self.path = self.path_value.get()
        self.folder_name = self.path.rsplit("\\",1)[1]
        #print(self.folder_name) 

        #self.directory = self.path
        for folder_entry in os.scandir(self.path): #directory):
            self.folder_name = Path(folder_entry).stem
            #print(folder_entry.path)
            mergedObject = PdfFileMerger()

            for file_entry in os.scandir(folder_entry):
                self.file_name = Path(file_entry).stem
                print("Filenname", self.file_name)


                if not (file_entry.path.endswith(".jpg")
                        or  file_entry.path.endswith(".jpeg")
                        or file_entry.path.endswith(".png")
                        #or file_entry.path.endswith(".doc")
                        or file_entry.path.endswith(".docx")
                        or file_entry.path.endswith(".pdf")
                        )and file_entry.is_file():
                        print("Was ist das? Konvertier ich nicht  " + file_entry.path)
                        
                #if (file_entry.path.endswith("") and file_entry.is_file()):
                #        print("nothing")

                

                        

                if (file_entry.path.endswith(".jpg") or  file_entry.path.endswith(".jpeg") or file_entry.path.endswith(".png")) and file_entry.is_file():
                        #print(file_entry.path) 

                        image = Image.open(file_entry.path)
                        i = image.convert('RGB')
                        i.save(os.path.splitext(file_entry.path)[0] + ".pdf")

               # if (file_entry.path.endswith(".doc") ) and file_entry.is_file():
               #         convert(file_entry)
	                        

                if (file_entry.path.endswith(".docx")) and file_entry.is_file():
                        convert(file_entry)

            for file_entry in os.scandir(folder_entry):    
                if (file_entry.path.endswith(".pdf") and file_entry.is_file()):
                    #print(file_entry.path + ".pdf")
                    
                    new_pdf = Pdf.new()
                    with Pdf.open(file_entry.path, allow_overwriting_input=True) as pdf:
                        pdf.save(file_entry.path)
                        
                    mergedObject.append(PdfFileReader(file_entry.path, "rb"))

            mergedObject.write(self.path + "\\" + Path(folder_entry).stem + " - " +Path(self.path).stem  + ".pdf")
        

root = tk.Tk()
app = Application(master=root)
app.mainloop()
