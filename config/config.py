#!/usr/bin/python

import json

class Config:
	def __init__(self):
		self.config_path = "/Users/asmuniz/Desktop/config-files/config.json"
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

	def cmdline(self):
		from optparse import OptionParser
		parser = OptionParser()
		parser.add_option("-d", "--data-path", dest='datapath', help='set path to data.json')
		parser.add_option("-e", "--email-login", dest='emailusr', help='set email login user')
		parser.add_option("-p", "--email-pwd", dest='emailpwd', help='set password for login email')
		parser.add_option("-l", "--email-list", dest='emails', help='set list of emails to send notifications to')
		parser.add_option("-a", "--add-email", dest='emailadd', help='add email to list')
		parser.add_option("--email-login-path", dest='loginpath', help='set path to emailcred.json')
		parser.add_option("--emails-path", dest='emailspath', help='set path to emails.json')
		parser.add_option("-r", "--remove-email", dest='emailrem', help='remove email from list')

		(options, args) = parser.parse_args()

		if options.datapath:
			self.setdatapath(options.datapath)

		if options.emailusr:
			self.setemailusr(options.emailusr)

		if options.emailpwd:
			self.setemailpwd(options.emailpwd)

		if options.emails:
			emails = []
			for email in options.emaillist.split(','):
				emails.append(email)
			self.setemaillist(emails)

		if options.emailadd:
			self.emaillist().append(options.emailadd)

		if options.loginpath:
			self.paths['emailcreds'] = options.loginpath

		if options.emailspath:
			self.paths['emaillist'] = options.emailspath

		if options.emailrem and options.emailrem in self.emaillist():
			self.emaillist().remove(options.emailrem)

		self.save()

		self.printConfig()

	def printConfig(self):
		print "\nCurrent configuration setup:**************\n"
		print "file paths:"
		print "\tconfig path: " + self.config_path
		print "\tdata path: " + self.datapath()
		print "\temail login path: " + self.paths['emailcreds']
		print "\temail list path: " + self.paths['emaillist']
		print "\nemail login:"
		print "\tuser: " + self.emailusr()
		print "\tpass: " + self.emailpwd()
		print "\nnotified emails:"
		for email in self.emaillist():
			print "\t" + email
		print "\n******************************************\n"

if __name__ == "__main__":
	c = Config()
	c.cmdline()
	"""
	print c.datapath()
	print c.emailusr()
	print c.emailpwd()
	print c.emaillist()
	c.setdatapath('/Users/asmuniz/Desktop/data.json')
	#c.save()
	"""
