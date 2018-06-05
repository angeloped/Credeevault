#!/usr/bin/env python

"""
MIT License

Copyright (c) 2018 Bryan Angelo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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