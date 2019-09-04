#########################################################	
#							#							
#This file is the main UI File which is responsible	#
#for running the whole OCR program          		#
#							#						
#########################################################
import os
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfilename
import voter_id_ocr_module
from voter_ID_parser import ParsePAN
import passport_code
import pan_ocr_parser
from parser_pan import Parse_PAN_1
import pan_code_old
import YOLO_py
import Yolo_DL_py

fields = ' Name','Fathers Name','Gender', 'Date of Birth','DL_No','Passport No.','Permanent Account Number Card','AADHAR NO.'
doc_picked=""


#####################################################################
#								#						
# Method: process (Function to fill the entries of the form.)	#	
# Parameter: Data Entries from dictionary.	      		#		
# Return: It returns nothing.					#					
#								#						            
#####################################################################
def process(entries):
	titleText = "Choose " + docBox.get() +" in " + imageBox.get() + " format"
	path = askopenfilename(initialdir="samples_OCR/",
	filetypes =(("JPG File","*.jpg"),("JPEG File", "*.jpeg"),("PNG Files","*.png"),("PDF Files","*.pdf")),
	title = titleText
	)
	values= {' Name': None,'Passport No.': None,'Gender':None,'Fathers Name':None,'DL_No': None ,'Date of Birth':None,'Permanent Account Number Card':None,'AADHAR NO.':None}


	res=format(chkValue.get())
	qr_bool=int(res)


	if doc_picked=="PAN_CARD_NEW":
		temp = pan_ocr_parser.helper(path)
		values = Parse_PAN_1.tmp_main(temp)

	elif doc_picked=="PAN_CARD_OLD":
		values = pan_code_old.helper(path)

	elif doc_picked=="AADHAR":
		values = YOLO_py.helper(path,qr_bool)

	elif doc_picked=="Voter_ID":
		print("Document selected is :", doc_picked)
		temp=voter_id_ocr_module.ocr_main1(path,False)
		values=ParsePAN.main_temp(temp)

	elif doc_picked=="PASSPORT":
		print("Document selected is :", doc_picked)
		values = passport_code.helper(path)

	elif doc_picked=="DL":
		print("Document selected is :", doc_picked)
		values = Yolo_DL_py.helper(path)

	print(values)
	for entry in entries:
		if entry:
			if entry[0] in values:
				text1  = entry[1].get()
				if len(text1)==0: 
					entry[1].insert(0,values[entry[0]])
	


def save(entries):
    filep = open("ocrdata.txt","w+")
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        print('%s: "%s"' % (field, text))
        filep.write('%s: "%s" ' % (field, text))
    filep.close


def makeform(root, fields):
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries
#########################################################################
#       This function is to check the document type selected.		#
#########################################################################
def on_select(event=None):
    if event:
    	global doc_picked
    	doc_picked=event.widget.get()

#########################################################################
#       This function is to clear the data entries in the form.		#
#########################################################################
def clear(entries):
      for entry in entries:
          endindex  = len(entry[1].get())                                                                                                                                                                 
          entry[1].delete(0,endindex)


#########################################################################################
#       This is the main function to carry out the oprations of the tkinter form.	#
#########################################################################################

if __name__ == '__main__':

    root = tk.Tk()
    root.title("Calsoft OCR Window")   
    entries = makeform(root, fields)

    # Create Image Type select box
    imageType = ["JPG","JPEG","PNG","PDF"]
    docType = ["PASSPORT", "DL","Voter_ID", "PAN_CARD_NEW","PAN_CARD_OLD","AADHAR"]
    imageLabel = tk.Label(root, text = "Image Type")
    imageLabel.pack(side=tk.LEFT, padx=5, pady=5)
    imageBox = ttk.Combobox(root, values = imageType)
    imageBox.pack(side=tk.LEFT, padx=5, pady=5)
    imageBox.current(0)
    imageBox.bind("<<ComboboxSelected>>")

    # Create Document Type select box
    docLabel = tk.Label(root, text = "DOC Type")
    docLabel.pack(side=tk.LEFT, padx=5, pady=5)
    docBox = ttk.Combobox(root, values = docType)
    docBox.pack(side=tk.LEFT, padx=5, pady=5)
    docBox.current(0)
    docBox.bind("<<ComboboxSelected>>",on_select)
   

    chkValue = IntVar(value=1)
    qrBox = tk.Checkbutton(root, text="Use QR", onvalue = 1, offvalue = 0, var=chkValue)
    qrBox.pack(side=tk.LEFT, padx=5, pady=5)

    docBox.bind("<<CheckbuttonSelected>>")

    # Process Button
    b1 = tk.Button(root, text='Upload', command=(lambda e=entries: process(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    # Save Button
    b2 = tk.Button(root, text='Save', command=(lambda e=entries: save(e)))
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    # Quit Button
    b2 = tk.Button(root, text='Close', command=root.quit)
    b2.pack(side=tk.LEFT, padx=5, pady=5)

    b3 = tk.Button(root, text='Clear', command=(lambda e=entries: clear(e)))
    b3.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()

