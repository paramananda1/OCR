#########################################################	
#							#
#	     This file is for the Passport OCR.         #
#							#
#########################################################
import numpy as np 
from passporteye import read_mrz
#########################################################################
#									#
# Method: Helper (Function to convert string into readable format)	#
# Parameter: Document Path as a string.	      				#
# Return: It returns a dictionary.					#
#									#
#########################################################################

def helper(doc_path):
	mrz = read_mrz(doc_path)
	string = str(mrz)
	pos = string.find("]")
	str_length = len(string)
	dict1 = {}
	arr_pos = []
	count = 0

	while pos < str_length:
		if string[pos]==',':
			arr_pos.append(pos)
		if string[pos]==')':
			arr_pos.append(pos)
		pos+=1


#############################################################
#   This function is to convert string into parsable text.  #
#############################################################
	def convert_to_text(text):
		lines = text.splitlines();
		result = 'NULL'
		for line in lines:
			if not line.strip():
				continue
			else:
				result = result + "\n" + line
		return result;
#########################################################################
#   This function is to create the respective field value from string   #
#########################################################################
	def create_word(num):
		char = ''
		count = arr_pos[num]
		while count < arr_pos[num+1]:
			if string[count].isalnum():
				char = char + string[count]
			count+=1
		return char
#################################################################
#     This function is to convert date into readable format   	#
#################################################################
	def reverse(string):
		year = string[0] + string[1]
		month = string[2] + string[3]
		date = string[4] + string[5]

		return date + '/' + month + '/' + year

	try:
		dict1['Passport No.'] = create_word(0)
		dict1[' Name'] = create_word(1) + ' ' + create_word(2)
		dict1['Gender'] = create_word(3)
		dict1['Date of Birth'] = reverse(create_word(4))
		
	except:# Error(Exception):
		print("Please select a VALID image")

	str1 = str(dict1)

	return dict1

