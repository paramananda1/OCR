################################################################
#								#
#	        This file is for Voter ID Card          	#
#								#
#################################################################
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
import matplotlib.pyplot as plt
import pyzbar.pyzbar as pyzbar
import OCRUI

#########################################################################
#									#
# Method: image_pre_process (Function to improve image quality) 	#
# Parameter: It accepts image as parameter.	      			#
# Return: It returns a image.						#
#									#
#########################################################################

def image_pre_process(image):
	kernel = np.ones((3,3), np.uint8) 

	image_to_resize=image
	#image_to_resize= autocrop_image(doc_path)
	length_x, width_y = image_to_resize.size
	factor = min(1, float(1024.0 / length_x))
	size = int(factor * length_x), int(factor * width_y)
	image_resized = image_to_resize.resize(size, Image.ANTIALIAS)
	#image_resized.show()

	#converting from PIL to OpenCV format
	open_cv_image = numpy.array(image_resized) 
	grayscaled = cv2.cvtColor(open_cv_image,cv2.COLOR_BGR2GRAY)

	# Thresholding the image
	(thresh, img_bin) = cv2.threshold(grayscaled, 0, 255, cv2.THRESH_BINARY | 		cv2.THRESH_OTSU)  
	img_bin = 255-img_bin 
	return img_bin


#########################################################################
#									#
# Method: QR_check (Function to check if QR is enabled.)         	#
# Parameter: It accepts image as parameter.	      			#
# Return: It returns nothing.						#
#									#
#########################################################################

def QR_check(image):
	decodedObjects = pyzbar.decode(image)
	#print(str(type(decodedObjects)))
	image_copy=image.copy()
	#if decodedObjects is NULL then go to tesseract, else display the QR info and skip tesseract operation
	temp='NULL'
	if not decodedObjects:
		temp=image_processing(image_copy)
		return temp
	else:
		for obj in decodedObjects:
			print('Type : ', obj.type)
			print('Data : ', obj.data,'\n')
	
########################################################################
#									#
# Method: image_processing (Function to convert image to string)	#
# Parameter: It accepts image as parameter.	      			#
# Return: It returns a data string.					#
#									#
#########################################################################
def image_processing(image):

	img_bin=image_pre_process(image)
	tess_image_Result = pytesseract.image_to_string(img_bin, lang= 'eng')

	lines = tess_image_Result.splitlines();
	result='NULL'
	for line in lines:
		if not line.strip():
			continue
		else:
			result = result+"\n"+re.sub(r"\s+"," ", line, flags = re.I) 
	return result


#########################################################################
#									#
# Method: pdf_to_image (Function to convert pdf pages to image)		#
# Parameter: Document Path as a string.	      				#
# Return: It returns a data string.					#
#									#
#########################################################################
def pdf_to_image(doc_path):
	#print("\nDOC type "+magic.from_file(doc_path))
	pages = convert_from_path(doc_path, 500) 
	total_data_from_pages='NULL'

	length=len(pages)
	for page in range(length): 
	    text= image_processing(pages[page])
	    total_data_from_pages= total_data_from_pages +text

	return total_data_from_pages	
#########################################################################
#									#
# Method: ocr_main1 (Main function to process the Voter ID Card)	#
# Parameter: Document Path as a string and QR bool value.		#
# Return: It returns a data string.					#
#									#
#########################################################################
def ocr_main1(doc_path,QR_flag):
	if "PDF" in magic.from_file(doc_path): 
		result_from_tesseract=pdf_to_image(doc_path)
	else:
		image=Image.open(doc_path)
		if QR_flag:
			result_from_tesseract=QR_check(image)
		else:
			result_from_tesseract=image_processing(image)
	
	return result_from_tesseract

