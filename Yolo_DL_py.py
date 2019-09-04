#########################################################	
#							#
#	  This is the parser file for Driving License   #
#							#
#########################################################
import os
from imutils import paths
import argparse
import imutils
import cv2
import magic
import re
import numpy as np
import pytesseract
from PIL import Image
import QR_reader
##########################################################################
#									##
# Method: destroy (Function to delete the data regarding image)		##
# Parameter: A folder							##
# Return: It returns nothing.						##
#									##
##########################################################################
def destroy(folder):
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		if os.path.isfile(file_path):
			os.unlink(file_path)

#########################################################################
#									#
# Method: Yolo_DL (Function to run Yolov3 detector on DL)		#
# Parameter 1: Document Path as a string.				#
# Parameter 2: A destination folder to process data  from image.	#
# Parameter 3: A dictionary to save extracted data .			#
# Return: It returns a dictionary.					#
#									#
#########################################################################
def Yolo_DL(doc_path,folder,dictionary2):
	DL_path_dir="DL_MH_dataset/data"
	DL_yolo_command="./darknet detector test "+(DL_path_dir)+"/obj.data "+(DL_path_dir)+"/yolov3-tiny.cfg "+ (DL_path_dir)+"/yolov3-tiny_final.weights "+(doc_path)
#./darknet detector test /obj.data /yolov3-tiny.cfg /yolov3-tiny_6000.weights
	print("\nCommand Given: \n"+DL_yolo_command)
	os.system(DL_yolo_command)
	#Dictionary as per bounding boxes of YOLO
	dictionary = {'Name': ' ', 'DL_No': ' ','Fathers Name':' ','DOB':' '}




	
	for filename in os.listdir(folder):
		image = cv2.imread(os.path.join(folder,filename))
		temp=os.path.basename(filename)
		temp2=os.path.splitext(temp)[0]
		img = cv2.resize(image, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
		tess_image_Result = pytesseract.image_to_string(img)
		dictionary2[temp2]=tess_image_Result


	destroy(folder)
	return dictionary2

def clean(dict1):
	dict1['DL_No'] = re.sub(r'\W+', '',dict1['DL_No'])
	dict1[' Name'] = re.sub("[^a-zA-Z]+", " ", dict1[' Name'])
	dict1['Fathers Name'] = re.sub("[^a-zA-Z]+", " ", dict1['Fathers Name'])
	return dict1

#########################################################################
#									#
# Method: Helper (Function to convert string into dictionary)		#
# Parameter: Document Path as a string and QR bool value.	      	#
# Return: It returns a dictionary.					#
#									#
#########################################################################

def helper(doc_path):

	
	dictionary2={' Name':'','DL_No': '', 'Fathers Name':'','Date of Birth': ''}
	folder='results'
	if not os.path.exists(folder):
		os.makedirs(folder)
	else:
		destroy(folder)
	dictionary2=Yolo_DL(doc_path,folder,dictionary2)
	dictionary2=clean(dictionary2)

	return dictionary2
