#!/usr/bin/python

import json

class Config:
	def __init__(self):
		self.config_path = "/Users/asmuniz/Desktop/config.json"
		f = open(self.config_path, 'r')
		self.paths = json.loads(f.read())
		f.close()
		
		# extract email credentials
		credfile = open(self.paths['emailcreds'], 'r')
		self.credJson = json.loads(credfile.read())
		credfile.close()

		self.email_dict = {}
		emailfile = open(self.paths['emaillist'], 'r')
		self.email_dict = json.loads(emailfile.read())
		emailfile.close()

	def datapath(self):
		return self.paths['datapath']

	def emailusr(self):
		return self.credJson['emailusr']

	def emailpwd(self):
		return self.credJson['emailpwd']

	def emaillist(self):
		return self.email_dict['emails']

	def setdatapath(self, path):
		self.paths['datapath'] = path

	def setemailusr(self, usr):
		self.credJson['emailusr'] = usr

	def setemailpwd(self, pwd):
		self.credJson['emailpwd'] = pwd

	def setemaillist(self, email_list):
		self.email_dict['emaillist'] = email_list

	def save(self):
		f = open(self.paths['emailcreds'], 'w')
		f.write(json.dumps(self.credJson, indent=4))
		f.close()

		f = open(self.paths['emaillist'], 'w')
		f.write(json.dumps(self.email_dict, indent=4))
		f.close()

		f = open(self.config_path, 'w')
		f.write(json.dumps(self.paths, indent=4))
		f.close()

if __name__ == "__main__":
	c = Config()
	print c.datapath()
	print c.emailusr()
	print c.emailpwd()
	print c.emaillist()
	c.setdatapath('/Users/asmuniz/Desktop/data.json')
	c.save()
