#!/usr/bin/env python
import os
import pyaes
import base64
import UniKee
import sqlite3
from time import time
from hashlib import md5
from subprocess import Popen
#Popen("mycmd" + " myarg", shell=True) equivalent to >> os.system("mycmd" + "myarg")
#DEBUG NOTE: add error handler in all input.
#I'm sorry for the WET method that I've commited.
#prone to SQL injection.
#add conn.commit
Desktop_loc = "/root/Desktop/"

class PACRUN:
	def __init__(self, UniKee_key):
		self.UniKee_key = UniKee_key
	def encrypt(self,key,data):
		return pyaes.AESModeOfOperationCTR(key).encrypt(data)
	def decrypt(self,key,data):
		return pyaes.AESModeOfOperationCTR(key).decrypt(data)
	def run(self):
		while self.UniKee_key:
			slice = self.UniKee_key[:100000]
			self.UniKee_key = self.UniKee_key[100000:]
			yield slice
	def assemble(self, data):
		for slice in self.run():
			data = self.encrypt(md5(slice).hexdigest(),data)
		return base64.b64encode(data)
	def disassemble(self, data):
		data = base64.b64decode(data)
		for slice in self.run():
			data = self.decrypt(md5(slice).hexdigest(),data)
		return data

with open("test.UniKee") as f:
	UniKee = f.read()
encryp = PACRUN(UniKee).assemble("OK")
decryp = PACRUN(UniKee).disassemble(encryp)
print("Encrypt: " + encryp)
print("Decrypt: " + decryp)