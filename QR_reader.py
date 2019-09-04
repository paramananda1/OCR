#########################################################	
#							#
#   This file is for Reading the QR data from image.    #
#							#
#########################################################
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
from PIL import Image 
import shlex

#########################################################################
#									#
# Method: decode (Function to decode qr image into the data string)	#
# Parameter: It accepts image as argument.				#
# Return: It returns a string.		      				#
#									#
#########################################################################
def decode(img) : 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(img)
  # Print results
  res = ""
  for obj in decodedObjects:
  	res = res + obj.data.decode() + "\n"
  return res
 
#########################################################################
#									#
# Method: Helper (Function to convert QR image into dictionary)	    	#
# Parameter: No parameter.	      					#
# Return: It returns a dictionary.					#
#									#
#########################################################################
def helper():
  # Read image
  dictionary2={' Name':' ','Gender': ' ', 'AADHAR NO.':' ','Date of Birth': ' '}
  src_path = "results/QR.jpg"

 # img=Image.open(src_path)
  img= cv2.imread(src_path)
  img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  decodedObjects = decode(img)
  print(decodedObjects)
  print("\nWorking\n")

  abc=shlex.split(decodedObjects)


  matching = [s for s in abc if "uid" in s]
  matching=str(matching).replace("uid=", "").replace('[','').replace("'",'').replace("'",'').replace(']','')
  dictionary2['AADHAR NO.']=str(matching)

  matching = [s for s in abc if "name" in s]
  matching=str(matching).replace("name=", "").replace('[','').replace("'",'').replace("'",'').replace(']','')
  dictionary2[' Name']=str(matching)

  matching = [s for s in abc if "gender" in s]
  matching=str(matching).replace("gender=", "").replace('[','').replace("'",'').replace("'",'').replace(']','')
  dictionary2['Gender']=str(matching)

  matching = [s for s in abc if "yob" in s]
  matching=str(matching).replace("yob=", "").replace('[','').replace("'",'').replace("'",'').replace(']','')
  dictionary2['Date of Birth']=str(matching)


  return dictionary2
