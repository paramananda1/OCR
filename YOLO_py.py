#########################################################	
#							#
#	   This is the parser file for Aadhar Card      #
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

#########################################################################
#									#
# Method: destroy (Function to delete the data regarding image)		#
# Parameter: A folder							#
# Return: It returns nothing.						#
#									#
#########################################################################
def destroy(folder):
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		if os.path.isfile(file_path):
			os.unlink(file_path)

#########################################################################
#									#
# Method: Yolo_Aadhar (Function to run Yolov3 detector on Aadhar)	#
# Parameter 1: Document Path as a string.				#
# Parameter 2: A destination folder to process data  from image.	#
# Parameter 3: A dictionary to save extracted data .			#
# Return: It returns a dictionary.					#
#									#
#########################################################################
def Yolo_Aadhar(doc_path,folder,dictionary2):
	aadhar_path_dir="aadhar-dataset/data"
	aadhar_yolo_command="./darknet detector test "+(aadhar_path_dir)+"/obj.data "+(aadhar_path_dir)+"/yolov3-tiny.cfg "+ (aadhar_path_dir)+"/yolov3-tiny_6000.weights "+(doc_path)
#./darknet detector test /obj.data /yolov3-tiny.cfg /yolov3-tiny_6000.weights
	print("\nCommand Given: \n"+aadhar_yolo_command)
	os.system(aadhar_yolo_command)
	#Dictionary as per bounding boxes of YOLO
	dictionary = {'name': ' ', 'gender': ' ','AADHAR NO.':' ','DOB':' '}
	#dictionary2={' Name':' ','Gender': ' ', 'AADHAR NO.':' ','Date of Birth': ' '}

	#folder='results'
	for filename in os.listdir(folder):
		image = cv2.imread(os.path.join(folder,filename))
		temp=os.path.basename(filename)
		temp2=os.path.splitext(temp)[0]
		#grayscaled = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		tess_image_Result = pytesseract.image_to_string(image)
		dictionary2[temp2]=tess_image_Result


	destroy(folder)
	return dictionary2

#########################################################################
# Method: Helper (Function to convert string into dictionary)		#
# Parameter: Document Path as a string and QR bool value.	      	#
# Return: It returns a dictionary.					#
#									#
#########################################################################

def helper(doc_path,QR):

	dictionary2={' Name':' ','Gender': ' ', 'AADHAR NO.':' ','Date of Birth': ' '}
	folder='results'
	if not os.path.exists(folder):
		os.makedirs(folder)
	else:
		destroy(folder)
	if QR==1:
		qr_path_dir="QR_dataset/data"
		qr_yolo_command="./darknet detector test "+(qr_path_dir)+"/obj.data "+(qr_path_dir)+"/yolov3-tiny.cfg "+ (qr_path_dir)+"/yolov3-tiny_final.weights "+(doc_path)
		print("\nCommand Given: \n"+qr_yolo_command)
		os.system(qr_yolo_command)

		#for imagePath in paths.list_images(args["images"]):
		for filename in os.listdir(folder):
			image = cv2.imread(os.path.join(folder,filename))
			#grayscaled = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
			dictionary3 = QR_reader.helper()

		if not bool(dictionary3['Gender']):
		    print("Dictionary is  empty, running Aadhar YOLO")
		    dictionary2=Yolo_Aadhar(doc_path,folder,dictionary2)
		else:
		    dictionary2.update(dictionary3)	


		destroy(folder)
	else:

		dictionary2=Yolo_Aadhar(doc_path,folder,dictionary2)

	return dictionary2
