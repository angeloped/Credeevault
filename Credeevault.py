#!/usr/bin/env python2

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

import os
import time
import pyaes
import base64
import UniKee
import sqlite3
from hashlib import md5
from subprocess import Popen
# DEBUG NOTE: add error handler in all input.
# I'm sorry for the WET method that I've commited.
# prone to SQL injection.
# UniKee should be found easily
# vault should have a name, too.
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

class Credeevault(PACRUN):
	def __init__(self):
		self.UniKee_key = ""
		self.vault_loc = ""
	def search_UniKee(self):
		# search UniKee algorithm
		UniKee = []
		for path in os.walk(Desktop_loc):
			for each_file in path[2]:
				if ".UniKee" in each_file[-6:]:
					vault.append((path[0] + "/" + each_file).replace("//","/"))
		return UniKee
	def access_UniKee(self):
		UniKee_key = ""
		# access UniKee in this block.
		while 1:
			do_have = raw_input("Do you have UniKee? (Y/n): ")
			if (do_have == "y" or do_have == "Y") or (do_have == "YES" or do_have == "yes"):
				#WIP
				list_UnieKee = self.search_UniKee()
				
				# FATAL ERROR
				
				print("List of scanned UniKee(s): \n")
				if len(list_UnieKee) > 0:			
					count_u = 0
					for e_UniKee in list_UniKee:
						print("[{0}] - {1}".format(count_u, e_UniKee))
						count_u += 1
				else:
					print("No UniKee have found.")
				
				what_name = raw_input("What is the name of your UniKee in \nthe Desktop? (ex: this_is_my.UniKee): ")
				if os.path.exists(Desktop_loc + what_name):
					#open UniKee
					with open(Desktop_loc + what_name) as readUniKee:
						UniKee_key = readUniKee.read()
					
					if len(UniKee_key) >= 1000000:
						break
					else: 
						print("WARNING! '{0}' is not a UniKee.".format(Desktop_loc + what_name))
				else:
					print("UniKee not found! You must put your UniKee in the Desktop.")
			elif (do_have == "n" or do_have == "N") or (do_have == "NO" or do_have == "no"):
				# naming
				while 1:
					UniKee_name = raw_input("What name of your UniKee should be? (example: Raz.UniKee): ")
					UniKee_name = UniKee_name.split(".UniKee")[0].split(".Unikee")[0].split(".unikee")[0]
					
					if UniKee_name == "":
						print("Do not use blank name!")
					else:
						break
					
				# prevent entering common password.
				while 1:
					new_passcode = raw_input("To generate your new UniKee. You must put a passcode: ")
					
					with open("password.txt") as passlist:
						existing_pass = passlist.read().split("\n")
						
					if new_passcode in existing_pass:
						print("WARNING! Passcode is common! Try a new passcode..")
					else:
						break
				
				start_time = time.time()
				UniKee_key = UniKee.diveee(new_passcode)
				
				if os.path.exists(Desktop_loc + UniKee_name + ".UniKee"):
					# find non-existing UniKee filename
					i=0
					while 1:
						unikname = Desktop_loc + UniKee_name + "({0}).UniKee".format(i)
						if not os.path.exists(unikname):
							break
						i += 1
					
					# create new UniKee
					with open(unikname,"w+") as newUniKee:
						newUniKee.write(UniKee_key)
						
				else:
					unikname = Desktop_loc + UniKee_name + ".UniKee"
					# create new UniKee
					with open(unikname,"w+") as newUniKee:
						newUniKee.write(UniKee_key)
						
				# done
				print("Time finished: {0} seconds".format(time.time() - start_time))
				print("Finished! Your new Unikee is located at '{0}'.".format(unikname))
				break
			else:
				print(".\nError! Please choose yes or no...")
			
		#print("Your UniKee opened sucessfully!")
		return UniKee_key
	def search_vault(self):
		# search vault algorithm
		vault = []
		for path in os.walk(Desktop_loc):
			for each_file in path[2]:
				if ".vault" in each_file[-6:]:
					vault.append((path[0] + "/" + each_file).replace("//","/"))
		return vault
	def new_vault(self):
		while 1:
			# get the name
			new_vaultname = raw_input("Enter new vault name (example: my_vault): ")
			
			# UniKee to access the vault.
			print("At this time, you need to access your UniKee.")
			self.UniKee_key = self.access_UniKee()
			
			pathfile = Desktop_loc + new_vaultname
			if os.path.exists(pathfile):
				print("{0} already exist. Try another one.".format(file))
			else:
				# create path in Desktop
				os.mkdir(pathfile)
				
				# create database vault
				conn = sqlite3.connect(pathfile + "/" +new_vaultname + ".vault")
				
				# add credits table here
				cur = conn.execute("CREATE TABLE credits(ID CHAR(8) PRIMARY KEY NOT NULL, DOMAIN TEXT NOT NULL, USERNAME TEXT NOT NULL, PASSWORD TEXT NOT NULL, DATE CHAR(50) NOT NULL)")
				if cur:
					print("credits space created sucessfully!")
				else:
					print("credits space create failed...")
				
				#commit every action
				conn.commit()
				
				# verification table here
				cur = conn.execute("CREATE TABLE verfy(ID CHAR(50), DATA TEXT NOT NULL)")
				if cur:
					print("verfy created sucessfully!")
					
					# insert
					cur = conn.execute("INSERT INTO verfy(ID,DATA) VALUES (1, \"{0}\")".format(PACRUN(self.UniKee_key).assemble("OK")))
					if cur:
						print("vault identity created sucessfully!")
					else:
						print("vault identity create failed...")
				else:
					print("verfy space create failed...")
					print("vault identity create failed...")
				
				#commit every action
				conn.commit()
				
				# close connection
				conn.close()
				
				print("{0} created sucessfully.".format(new_vaultname + ".vault"))
				break
	def open_vault(self):
		vaults = self.search_vault()
		
		print("List of scanned vault(s): \n")
		if len(vaults) > 0:			
			while 1:
				count_v = 0
				for vault in vaults:
					print("[{0}] - {1}".format(count_v, vault))
					count_v += 1
				
				try:# WIP
					which_vault = input("Choose your vault to unlock (example 1): ")
					
					# selected vault
					self.vault_loc = vaults[which_vault]
					
					# connect here
					conn = sqlite3.connect(self.vault_loc)
					
					#then
					
					# UniKee to access the vault.
					print("At this time, you need to access your UniKee.")
					self.UniKee_key = self.access_UniKee()
					
					cur = conn.execute("SELECT * FROM verfy WHERE ID=1")
					
					for data in cur:
						data = data[1]
					
					#if matched then
					if PACRUN(self.UniKee_key).disassemble(data) == "OK":
						print("Access granted!")
						return True
					else:
						print("This UniKee is not the key to decrypt this vault.")
					
					# close connection
					conn.close()
				except:
					print("Error! Wrong input, try again.\nType 'main' to go to the main menu.\nLeave it blank if you don't.")
					command = raw_input("Enter command: ")
					if command == "main":
						break
		else:
			print("No vaults have found.")
			return False
	
	# #############
	#   command functions
	# #############
	def show_record(self):#WIP add logic
		# connect to the database
		
		# FATAL ERROR: self.vault_loc didn't set up correctly
		print("x:" + self.vault_loc)
		
		
		conn = sqlite3.connect(self.vault_loc)
		cur = conn.execute("SELECT * FROM credits")
		
		print("These are the records shown:")
		rec_exists = False
		
		for data in cur:
			print("ID: {0}; DOMAIN: {1}; USERNAME: {2}; PASSWORD: {3}; DATE: {4};".format(data[0], data[1], PACRUN(self.UniKee_key).disassemble(data[2]), PACRUN(self.UniKee_key).disassemble(data[3]), data[4]))
			rec_exists = True
		
		if not rec_exists:
			print("No records to be shown. Create a new record! :D")
		
		#close connection
		conn.close()
	def new_record(self):
		escape = False
		while 1:
			# generate 5 char hash from a random character as ID
			ID = md5(str(time.time())).hexdigest()[:5]
			
			# domain
			DOMAIN = raw_input("Enter domain/site of your account (example: facebook.com): ")
			
			# username & password
			USERNAME = raw_input("Enter the username of your account: ")
			PASSWORD = raw_input("Enter the password of your account: ")
			
			# time & date
			DATETIME = time.asctime()
			
			while 1:
				print("These will be saved:\nID: {0} ; DOMAIN: {1} ; USERNAME: {2} ; PASSWORD: {3} ; DATE: {4} ;".format(ID, DOMAIN, USERNAME, PASSWORD, DATETIME))
				
				# confirmation
				save_confirm = raw_input("Are you sure you want to save these? (Y/n):")
				if (save_confirm == "y" or save_confirm == "Y") or (save_confirm == "YES" or save_confirm == "yes"):
					# connect to the database
					conn = sqlite3.connect(self.vault_loc)
					
					# insert into the database
					cur = conn.execute("INSERT INTO credits(ID, DOMAIN, USERNAME, PASSWORD, DATE) VALUES (\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\")".format(ID, DOMAIN, PACRUN(self.UniKee_key).assemble(USERNAME), PACRUN(self.UniKee_key).assemble(PASSWORD), DATETIME))
					
					#commit every action
					conn.commit()
					
					#close connection
					conn.close()
					
					#done
					print("Saving done!")
					escape = True
					break
				elif (save_confirm == "n" or save_confirm == "N") or (save_confirm == "NO" or save_confirm == "no"):
					print("Saving canceled...")
					escape = True
					break
			if escape:
				break
	def delete_record(self):
		# show tables
		self.show_record()
		
		# ID selection
		ID_to_delete = raw_input("Select ID to delete record: ")
		while 1:
			# confirmation
			delete_confirm = raw_input("Are you sure you want to delete this? (Y/n):")
			if (delete_confirm == "y" or delete_confirm == "Y") or (delete_confirm == "YES" or delete_confirm == "yes"):
				# connect to the database
				conn = sqlite3.connect(self.vault_loc)
				
				# delete record from the database
				cur = conn.execute("DELETE FROM credits WHERE ID=\"{0}\"".format(ID_to_delete))
				
				#commit every action
				conn.commit()
				
				#close connection
				conn.close()
				
				#done
				print("Deleting done!")
			elif (delete_confirm == "n" or delete_confirm == "N") or (delete_confirm == "NO" or delete_confirm == "no"):
				print("Deletion canceled...")
				break
	def edit_record(self):
		# show tables
		self.show_record()
		
		# ID selection
		ID_to_delete = raw_input("Select ID to edit record: ")
		
		# #######
		#  edit stage
		# #######
		
		# domain
		DOMAIN = raw_input("Enter domain/site of your account (example: facebook.com): ")
		
		# username & password
		USERNAME = raw_input("Enter the username of your account: ")
		PASSWORD = raw_input("Enter the password of your account: ")
		
		# time & date
		DATETIME = time.asctime()
		
		# confirmation
		edit_confirm = raw_input("Are you sure you want to edit and save this? (Y/n):")
		if (edit_confirm == "y" or edit_confirm == "Y") or (edit_confirm == "YES" or edit_confirm == "yes"):
			# connect to the database
			conn = sqlite3.connect(self.vault_loc)
			
			# edit record from the database
			cur = conn.execute("UPDATE credits SET DOMAIN=\"{0}\", USERNAME=\"{1}\", PASSWORD=\"{2}\", DATE=\"{3}\" WHERE ID=\"{4}\"".format(DOMAIN, PACRUN(self.UniKee_key).assemble(USERNAME), PACRUN(self.UniKee_key).assemble(PASSWORD), DATETIME,ID_to_delete))
			
			#commit every action
			conn.commit()
			
			#close connection
			conn.close()
			#done
			print("Editing done!")
		elif (edit_confirm == "n" or edit_confirm == "N") or (edit_confirm == "NO" or edit_confirm == "no"):
			print("Editing canceled...")
	
	# ###########
	#    main function
	# ###########
	def mainfunc(self):
		while 1:
			print("""
			 [1] - create new vault
			 [2] - open your vault
			 [3] - exit
			""")
			option_main = input("Choose one (example: 1): ")
			if not option_main in [1,2,3,4]:
				print("Error! Please enter a correct input.")
			elif option_main == 1:
				# create new vault
				self.new_vault()
			elif option_main == 2:
				# open new vault
				if self.open_vault():
					while 1:
						print("""
						[1] - new record
						[2] - edit record
						[3] - show records
						[4] - delete record
						[5] - Logout vault
						""")
						vault_options = input("Choose one (example: 0): ")
						if not vault_options in [1,2,3,4,5]:
							print("Error! Please enter a correct input.")
						elif vault_options == 1:
							self.new_record()
						elif vault_options == 2:
							self.edit_record()
						elif vault_options == 3:
							self.show_record()
						elif vault_options == 4:
							self.delete_record()
						elif vault_options == 5:
							print("Logging out...")
							
							# garbage collection
							del self.UniKee_key
							del self.vault_loc
							
							self.UniKee_key = self.vault_loc = ""
							print("Logged out!")
							break
						
			elif option_main == 3:
				# exit or quit program
				exit()
				quit()
	

if __name__ == "__main__":
	Credeevault().mainfunc()