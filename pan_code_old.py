##########################################################	
#							##
#	   This file is for Old Format of Pan Card      ##
#							##
##########################################################
import cv2
import magic
import numpy
import pdf2image
import numpy as np
import pytesseract
import re
from PIL import Image 
from pdf2image import convert_from_path 
from pytesseract import image_to_string
from matplotlib import pyplot as plt

#######################################################################
#									#
# Method: Helper (Function to convert string into readable format)	#
# Parameter: Document Path as a string.	      				#
# Return: It returns a dictionary.					#
#									#
#########################################################################

def helper(doc_path):
	def convert_to_text(text):
		lines = text.splitlines();
		result = 'NULL'
		for line in lines:
			if not line.strip():
				continue
			else:
				result = result + "\n" + line
		return result;

	def clean(dict1):
		dict1['Permanent Account Number Card'] = re.sub(r'\W+', '',dict1['Permanent Account Number Card'])
		dict1[' Name'] = re.sub("[^a-zA-Z]+", " ", dict1[' Name'])
		dict1['Fathers Name'] = re.sub("[^a-zA-Z]+", " ", dict1['Fathers Name'])
		dict1['Date of Birth'] = re.sub("[^0-9]+", "/", dict1['Date of Birth'])
		return dict1


	#### To check if file format is pdf
	if "PDF" in magic.from_file(doc_path): 

		pages = convert_from_path(doc_path) 

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

		imageResult3 = pytesseract.image_to_string(grayscaled, lang = 'eng')

		result = convert_to_text(imageResult3)



	i = 0
	n = len(result)
	num = 0
	dict1 = {' Name':'','Fathers Name':'','Date of Birth':'','Permanent Account Number Card':''}
	char1 = ''
	char2 = ''
	char3 = ''
	char4 = ''
	i = result.find("MENT")
	i+=4
	while i < n:
		try:

			if result[i]=='\n':
				num+=1
			if num==1:
				i = i+1
				while result[i+1]!='\n':
					char1 = char1 + result[i]
					i = i+1
			if num == 1:
				char1 = char1 + result[i]
			dict1[' Name'] = char1
			if num == 2:
				i = i+1
				while result[i+1]!='\n':
					char2 = char2 + result[i]
					i = i+1
			if num==2:
				char2 = char2 + result[i]
			dict1['Fathers Name'] = char2
			if num == 3:
				i = i+1
				while result[i+1]!='\n':
					char3 = char3 + result[i]
					i = i+1
			if num == 3:
				char3 = char3 + result[i]
			dict1['Date of Birth'] = char3
			if num == 5:
				i = i+1
				while result[i+1]!='\n':
					char4 = char4 + result[i]
					i = i+1
			if num == 5:
				char4 = char4 + result[i]
			dict1['Permanent Account Number Card'] = char4
			i = i+1
		except:
			print("Please enter a VALID image")
			for key in dict1:
				dict1[key] = []

			return dict1
	#print(dict1)
	dict1 = clean(dict1)
	return dict1
