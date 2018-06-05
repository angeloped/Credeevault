#!/usr/bin/env python
from hashlib import md5

class diveUniKee:
	def __init__(self, words):
		self.words = words
		self.UniKee = ""# your key
	def data_similarities(self, inputA, inputB): #input A always left
		char_similarities = ""
		for e_inputA in inputA:
			for e_inputB in inputB:
				if e_inputB in e_inputA and not e_inputB in char_similarities:
					char_similarities += e_inputB
		return char_similarities
	def uhm(self):
		while len(self.UniKee) <= 1000000:
			# slice into two
			half_div = len(self.words) // 2
			
			# convert each into hash
			word_a,word_b = md5(self.words[:half_div]).hexdigest(),md5(self.words[half_div:]).hexdigest()
			
			self.words = md5(word_a + word_b).hexdigest()
			
			# get all similarities and add
			self.UniKee += self.data_similarities(word_a,word_b)
			
			print("Generating {0} bits".format(len(self.UniKee)))
		return self.UniKee
def diveee(key_code):
	return diveUniKee(md5(key_code).hexdigest()).uhm()