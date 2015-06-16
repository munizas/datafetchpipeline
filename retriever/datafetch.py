import os.path
import urlparse
import re
import subprocess
import time

# sleep interval in seconds
ps_check_interval = 15

class FtpFetch:

	def __init__(self, netloc, collection, file_name_root, save_dir, *file_ext):
		self.cmd = ['wget']
		self.opts = ['--background', '--no-host-directories', '--recursive', '--server-response', '--timestamping']	

		self.scheme = 'ftp'
		self.netloc = netloc
		self.collection = collection
		self.file_name_root = file_name_root
		self.save_dir = save_dir
		self.opts += ['-P' + save_dir]

		for ext in file_ext:
			self.opts += ['-A' + file_name_root + '*' + ext]

	def fetch(self):
		path = os.path.join(self.collection)
		target = urlparse.urlunsplit((self.scheme, self.netloc, path, '', ''))
		log = '-o' + self.file_name_root + 'log'
		
		print 'running===============>', self.file_name_root
		
		p1 = subprocess.Popen( self.cmd+self.opts+[log]+[target],stdout=subprocess.PIPE)
		# blocking, based on backgrounded wget process:
		msg = p1.stdout.readline()
		pid = msg.split()[-1][:-1]
		rexp = re.compile( pid + '.*wget')
		while True:
		    p2 = subprocess.Popen( ['ps','-A'],stdout=subprocess.PIPE)
		    psAout = p2.stdout.read()
		    if re.search(rexp,psAout):
		        time.sleep(ps_check_interval)
		    else:
		        break

		print 'done', self.file_name_root, ':)'

	def __str__(self):
		return "scheme: " + self.scheme + "\nnetwork location: " + self.netloc + "\nfile_name_root: " + self.file_name_root + "\nsave_dir" + self.save_dir