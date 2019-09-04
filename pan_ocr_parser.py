############################################################
#							####
#	   This file is for New Format of Pan Card      ####
#							####
############################################################
import cv2
import magic
import re
import numpy
import pdf2image
import numpy as np
import pytesseract
from PIL import Image 
from pdf2image import convert_from_path 
from pytesseract import image_to_string
from matplotlib import pyplot as plt


#################################################################################################
#												#
# Method: Helper (Function to convert string into readable format and passing to parser file)	#
# Parameter: Document Path as a string.	      						        #
# Return: It returns a string.									#
#												#
#################################################################################################

def helper(doc_path):
	#### Function to convert string into readable format
	def convert_to_text(text):
		lines = text.splitlines();
		result = 'NULL'
		for line in lines:
			if not line.strip():
				continue
			else:
				result = result + "\n" + line
		return result;



	#### To check if file format is pdf
	if "PDF" in magic.from_file(doc_path): 

		pages = convert_from_path(doc_path, 500) 

		index = 1
		for page in pages:
			page.save("page_" + str(index) + ".jpg", 'JPEG')
			index += 1

		page_limit=index-1

		for p in range (1,page_limit+1):
			file_name="page_"+str(p)+".jpg"
			text =  str(((pytesseract.image_to_string(Image.open(file_name)))))

		result = convert_to_text(text)

	#### Else if file format is jpg,png,jpeg
	else:

		kernel = np.ones((3,3), np.uint8) 

		im = cv2.imread(doc_path)
		grayscaled = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

		th = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)

		retval2,threshold2 = cv2.threshold(grayscaled,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

		imageResult3 = pytesseract.image_to_string(threshold2)

		result = convert_to_text(imageResult3)
		#zprint(result)
	return result

#helper(doc_path)
