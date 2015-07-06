#!/usr/bin/python

import json

class Config:
	def __init__(self):
		self.config_path = "/Users/asmuniz/Desktop/config.json"
		f = open(self.config_path, 'r')
		jsonObj = json.loads(f.read())
		f.close()

		self.data_path = jsonObj['datapath']
		
		# extract email credentials
		credfile = open(jsonObj['emailcreds'], 'r')
		self.email_user = credfile.readline().rstrip('\n')
		self.email_pwd = credfile.readline().rstrip('\n')
		credfile.close()

		self.email_list = []
		emailfile = open(jsonObj['emaillist'], 'r')
		for email in emailfile:
			self.email_list.append(email.rstrip('\n'))
		emailfile.close()

	def datapath(self):
		return self.data_path

	def emailusr(self):
		return self.email_user

	def emailpwd(self):
		return self.email_pwd

	def emaillist(self):
		return self.email_list

	def hi(self):
		return 'hi'

if __name__ == "__main__":
	c = Config()
	print c.datapath()
	print c.emailusr()
	print c.emailpwd()
	print c.emaillist()
