##########################################################
#							##
#	   This is the parser file for new pan card     ##
#							##
##########################################################
import json
import difflib
import code
import re
class Parse_PAN_1:
	
	def __init__(self, autoConf=True, confFile="config.json", **kwargs):
		self.lineDelimiter = ""
		self.inLineDelimiter = "\n"
		self.keywords = ""
		self.file = ""
		self.consumeLines = 0
		self.txt = None
		self.parsedTxt = {}
		self.noiseSensitivity = 0.3	
		if autoConf == True:
			with open(confFile) as data:
				config = json.load(data)
				self.lineDelimiter = config["lineDelimiter"]
				self.inLineDelimiter = config["inLineDelimiter"]
				self.keywords = config["keywords"]
				self.file = config["file"]
				self.consumeLines = config["consumeLines"]
		else:
			self.lineDelimiter = kwargs["lineDelimiter"]
			self.keywords = kwargs["keywords"]
			if "file" in kwargs:
				self.file = kwargs["file"]
			else:
				self.txt = kwargs["txt"]
			if self.lineDelimiter == "\n":
				if "consumeLines" in kwargs:
					self.consumeLines = kwargs["consumeLines"]
				else:
					self.consumeLines = 1					
			if "inLineDelimiter" in kwargs:
				self.inLineDelimiter = kwargs["inLineDelimiter"]
			if "noiseSensitivity" in kwargs:
				self.noiseSensitivity = kwargs["noiseSensitivity"]
		if self.txt == None:
			with open(self.file) as inputTxt:
				self.txt = inputTxt.read()
#########################################################	
#							#
#Method:	findKeyword				#
#							#
#########################################################

	def findKeyword(self, line):
		line = line.lower()
		result = difflib.get_close_matches(line, self.keywords, cutoff=self.noiseSensitivity)
		if len(result) == 0:  
			return -1
		else:
			return result[0]

	def parse(self):
		lines = self.txt.split(self.lineDelimiter)
		parsed = {}
		keyword = None
		for index in range(0, len(lines)):
			if self.inLineDelimiter == "\n":
				keyword = self.findKeyword(lines[index])
				if keyword == -1:
					continue
				if self.consumeLines > 1:
					parsed[keyword] = [lines[i] for i in range(index+1, index+self.consumeLines+1) if i < len(lines)]
				else:
					if index+1 >= len(lines):
						break
					parsed[keyword] = lines[index+1]
			else:
				line = lines[index].split(self.inLineDelimiter)
				keyword = self.findKeyword(line[0])
				if keyword == -1:
					continue
				if len(line) == 2:
					parsed[keyword] = line[1]
				else:
					parsed[keyword] = [line[i] for i in range(1, len(line))]
		self.parsedTxt = parsed
		return self.parsedTxt
	
	def prettyPrint(self, seperator=":"):
		for key, val in self.parsedTxt.items():
			print(key+" "+seperator+" "+val)

#################################################################################################
#												#
# Method: clean (Function to remove the non relevent characters from respective fields)	        #
# Parameter: It takes Dictionary as a parameter.	      					#
# Return: It returns nothing.									#
#												#
#################################################################################################
	def clean(self):

		self.parsedTxt['Permanent Account Number Card'] = re.sub(r'\W+', '',self.parsedTxt['Permanent Account Number Card'])
		self.parsedTxt[' Name'] = re.sub("[^a-zA-Z]+", " ", self.parsedTxt[' Name'])
		self.parsedTxt['Fathers Name'] = re.sub("[^a-zA-Z]+", " ", self.parsedTxt['Fathers Name'])
		self.parsedTxt['Date of Birth'] = re.sub("[^0-9]+", "/", self.parsedTxt['Date of Birth'])

#################################################################################################
#												#
# Method: tmp_main (Function to convert passed string into dictionary)	                        #
# Parameter: It takes data string as a parameter.	      					#
# Return: It returns a dictionary.								#
#												#
#################################################################################################
	def tmp_main(string):
		toParse = string
		abc = Parse_PAN_1(autoConf=False, lineDelimiter="\n", inLineDelimiter="\n", consumeLines=1, keywords=[" Name", "Fathers Name","Sex","Son/Daughter/Wife of", "Date of Birth", "Permanent Account Number Card"], txt=toParse)

		try:
			abc.parse()
			abc.clean()
			#abc.prettyPrint()
		except:
			print("Please enter a VALID image")
			for key in abc.parsedTxt:
				abc.parsedTxt[key] = []

			return abc.parsedTxt
		return abc.parsedTxt

