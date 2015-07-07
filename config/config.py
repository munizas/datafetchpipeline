#!/usr/bin/python

import json
import os
import sys

class Config:
	def __init__(self):
		self.data_path = os.getcwd() + "/config/data.json"
		self.creds_path = os.getcwd() + "/config/emailcred.json"
		self.emails_path = os.getcwd() + "/config/emails.json"
		
		# extract email credentials
		credfile = open(self.creds_path, 'r')
		self.credJson = json.loads(credfile.read())
		credfile.close()

		self.email_dict = {}
		emailfile = open(self.emails_path, 'r')
		self.email_dict = json.loads(emailfile.read())
		emailfile.close()

	def datapath(self):
		return self.data_path

	def emailusr(self):
		return self.credJson['emailusr']

	def emailpwd(self):
		return self.credJson['emailpwd']

	def emaillist(self):
		return self.email_dict['emails']

	def setemailusr(self, usr):
		self.credJson['emailusr'] = usr

	def setemailpwd(self, pwd):
		self.credJson['emailpwd'] = pwd

	def setemaillist(self, email_list):
		self.email_dict['emaillist'] = email_list

	def save(self):
		f = open(self.creds_path, 'w')
		f.write(json.dumps(self.credJson, indent=4))
		f.close()

		f = open(self.emails_path, 'w')
		f.write(json.dumps(self.email_dict, indent=4))
		f.close()

	def cmdline(self):
		from optparse import OptionParser
		parser = OptionParser()
		parser.add_option("-e", "--email-login", dest='emailusr', help='set email login user')
		parser.add_option("-p", "--email-pwd", dest='emailpwd', help='set password for login email')
		parser.add_option("-l", "--email-list", dest='emails', help='set list of emails to send notifications to')
		parser.add_option("-a", "--add-email", dest='emailadd', help='add email to list')
		parser.add_option("-r", "--remove-email", dest='emailrem', help='remove email from list')

		(options, args) = parser.parse_args()

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

		if options.emailrem and options.emailrem in self.emaillist():
			self.emaillist().remove(options.emailrem)

		self.save()
		self.printConfig()

	def printConfig(self):
		print "\nCurrent configuration setup:**************\n"
		print "file paths:"
		print "\tdata path: " + self.datapath()
		print "\temail login path: " + self.creds_path
		print "\temail list path: " + self.emails_path
		print "\nemail login:"
		print "\tuser: " + self.emailusr()
		print "\tpass: " + self.emailpwd()
		print "\nnotified emails:"
		for email in self.emaillist():
			print "\t" + email
		print "\n******************************************\n"

if __name__ == "__main__":
	c = Config()
	if len(sys.argv) > 1:
		c.cmdline()
	else:
		c.printConfig()
