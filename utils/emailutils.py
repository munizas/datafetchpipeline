import smtplib

class GmailSend:
	def __init__(self, gmail_user, gmail_pwd, from_user, subject, text, to_users):
		self.gmail_user = gmail_user
		self.gmail_pwd = gmail_pwd
		self.from_user = from_user
		self.subject = subject
		self.text = text
		self.to_users = to_users # must be a list

	def send_email(self):
		# Prepare actual message
		message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
		""" % (self.from_user, ", ".join(self.to_users), self.subject, self.text)
		try:
		    #server = smtplib.SMTP(SERVER) 
		    server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
		    server.ehlo()
		    server.starttls()
		    server.login(self.gmail_user, self.gmail_pwd)
		    server.sendmail(self.from_user, self.to_users, message)
		    #server.quit()
		    server.close()
		    print 'successfully sent the mail'
		except:
		    print "failed to send mail"
