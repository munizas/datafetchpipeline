#!/usr/bin/python

"""
This module contains classes that can be used to fetch data from
specified servers.
"""

import os.path
import urlparse
import re
import subprocess
import time
import datetime
import errno
import urllib

# sleep interval in seconds
ps_check_interval = 15

class FtpFetch:
	"""
	Class that connects to an ftp site to retrieve data.
	"""

	def __init__(self, netloc, collection, file_name_root, save_dir, *file_ext):
		"""
		Args:
			netloc (string): the url of the ftp server
			collection (string): the path of the desired collection
			file_name_root (string): the root name of the desired files
			save_dir (string): the location to save the downloaded data
			*file_ext: variable length argument list that contains desired file extensions

			example use:

			fetchObj = FtpFetch("ftp.cdc.noaa.gov", "Datasets/ncep.reanalysis2/gaussian_grid", "shum.2m.gauss.", "/Users/asmuniz/ProjectCode/data/shum", "hdf", "xml", "nc")
		"""

		# path to wget
		self.cmd = ['/usr/local/bin/wget']
		# wget options
		self.opts = ['--background', '--recursive', '--server-response', '--timestamping', '-nd']	

		self.scheme = 'ftp'
		self.netloc = netloc
		self.collection = collection
		self.file_name_root = file_name_root
		self.save_dir = save_dir
		self.opts += ['-P' + save_dir]

		for ext in file_ext:
			self.opts += ['-A' + file_name_root + '*' + ext]

	def fetch(self):
		"""
			Starts the process to download the requested data.
		"""

		# setup target and log
		path = os.path.join(self.collection)
		target = urlparse.urlunsplit((self.scheme, self.netloc, path, '', ''))
		log = '-o' + self.file_name_root + 'log'
		
		print 'running===============>', self.file_name_root
		
		# start up a process to run wget
		p1 = subprocess.Popen( self.cmd+self.opts+[log]+[target],stdout=subprocess.PIPE)
		# blocking, based on backgrounded wget process:
		msg = p1.stdout.readline()
		pid = msg.split()[-1][:-1]
		rexp = re.compile( pid + '.*wget')
		while True:
			# start a process to run ps command with displays currently running processes
		    p2 = subprocess.Popen( ['ps','-A'],stdout=subprocess.PIPE)
		    psAout = p2.stdout.read()
		    if re.search(rexp,psAout): # if wget shows up as currently running then continue to sleep and check later
		        time.sleep(ps_check_interval)
		    else:
		        break

		print 'done downloading', self.file_name_root, ':)'
		print 'moving log file...'

		# make logs directory if doesn't exist
		logpath = self.save_dir+'/logs/'
		try:
			os.makedirs(logpath)
   		except OSError as exc:
   			if exc.errno == errno.EEXIST and os.path.isdir(logpath):
   				pass
   			else: raise

   		# move log file to logs directory
   		self.log_loc = logpath+str(datetime.date.today())+'-'+self.file_name_root+'log'
		os.rename(self.file_name_root+'log', self.log_loc)
		print 'log file moved...'

class USGSFetch:
	"""
	Fetch object that is designed to retrieve data from http://e4ftl01.cr.usgs.gov
	Currently the last-modified headers are not enabled on the server so timestamping is not available.
	--no-clobber is used to ensure existing files are not re-downloaded. This will, however, not retrieve updated files
	Implementation uses urllib to get list of files to download.
	"""

	def __init__(self, modis_terra, collection, save_dir, min_year, *file_ext):
		"""
		Args:
			modis_terra (string): select from ['ASTT', 'MOLA', 'MOLT', 'MOTA', 'SRTM', 'WELD'] check website for updates
			collection (string): the desired collection such as 'MOD13A1.005'
			save_dir (string): the location to save the downloaded data
			min_year (string): the minimum year to retrieve data
			*file_ext: variable length argument list that contains desired file extensions

			example use:

				fetchObj = USGSFetch('MOLT', 'MOD13A1.005', '/Users/asmuniz/ProjectCode/data/MOD13A1.005', "2015", "hdf", "xml", "nc")
		"""	

		self.cmd = ['/usr/local/bin/wget']
		self.opts = ['-Ahdf,xml', '--background', '--level=1', '--recursive', '--no-host-directories', '--server-response', '--no-clobber']

		self.scheme = 'http'
		self.netloc = 'e4ftl01.cr.usgs.gov'
		self.modis_terra = modis_terra
		self.collection = collection
		self.save_dir = save_dir
		self.opts += ['-P' + save_dir]
		self.min_year = min_year

		for ext in file_ext:
			self.opts += ['-A' + '*' + ext]

	def fetch(self):
		"""
		Starts the process to download the requested data
		"""

		# parse page to identify which files to download based in min_year
		cur_year = datetime.datetime.today().year
		download_list = []
		path = self.scheme + "://" + self.netloc + '/' + self.modis_terra + '/' + self.collection + '/'
		rf = urllib.urlopen(path)
		for line in rf.readlines():
			y = int(self.min_year)
			while y <= cur_year:
				mo = re.search(r"" + re.escape(str(y)) + "\.\d{2}\.\d{2}", line)
				if mo:
					download_list.append(mo.group())
					break
				y += 1
		rf.close()

		# local options:
		ps_check_interval = 15
		
		for s in download_list:
			# submit wget command, "block" on completion (by checking at regular intervals):
			target = path + s # urlparse.urlunsplit( ("http",netloc,path,query,fragment))
			log = '-o' + s + '.log'

			print 'running===============>', target

			p1 = subprocess.Popen(self.cmd + self.opts + [log] + [target], stdout=subprocess.PIPE)
			# blocking, based on backgrounded wget process:
			msg = p1.stdout.readline()
			pid = msg.split()[-1][:-1]
			rexp = re.compile(pid + '.*wget')
			while True:
				p2 = subprocess.Popen( ['ps','-A'],stdout=subprocess.PIPE)
				psAout = p2.stdout.read()
				if re.search(rexp,psAout):
					time.sleep(ps_check_interval)
				else:
					break

			print 'done downloading', s, ':)'
			print 'moving log file...'

			logpath = self.save_dir+'/logs/'
			print 'logpath = ' + logpath
			try:
				os.makedirs(logpath)
   			except OSError as exc:
   				if exc.errno == errno.EEXIST and os.path.isdir(logpath):
   					pass
   				else: raise

   			self.log_loc = logpath+str(datetime.date.today())+'-'+s+'.log'
   			print 'log_loc = ' + self.log_loc
			os.rename(s+'.log', self.log_loc)
			print 'log file moved...'

class NERSCFetch:
	"""
		Fetch object that is designed to retrieve data from https://portal.nersc.gov
		Currently the last-modified headers are not enabled on the server so timestamping is not available.
		--no-clobber is used to ensure existing files are not re-downloaded. This will, however, not retrieve updated files
		Implementation uses urllib to get list of files to download.
	"""

	def __init__(self, collection, save_dir, min_year, *file_ext):
		"""
		Args:
			collection (string): select from ['MOD04_L2', 'MOD05_L2', 'MOD06_L2', 'MOD07_L2', 'MOD11_L2', 'MYD04_L2', 'MYD05_L2', 'MYD06_L2', 'MYD07_L2', 'MYD11_L2']
				check website for updates
			save_dir (string): the location to save the downloaded data
			min_year (string): the minimum year to retrieve data
			*file_ext: variable length argument list that contains desired file extensions

			example use:

				fetchObj = NERSCFetch('MOD04_L2', '/Users/asmuniz/ProjectCode/data/MOD04_L2', "2013", "tar")
		"""	

		self.cmd = ['/usr/local/bin/wget']
		self.opts = ['--background', '--cut-dirs=5', '--level=1', '--no-host-directories', '--recursive', '-e robots=off', '--server-response', '--no-clobber']

		self.scheme = 'https'
		self.netloc = 'portal.nersc.gov'
		self.collection = collection
		self.save_dir = save_dir
		self.opts += ['-P' + save_dir]
		self.min_year = min_year

		for ext in file_ext:
			self.opts += ['-A' + '*' + ext]

		self.opts += ['-Ridx']

		self.grids = ("240", "1200")

	def fetch(self):
		"""
		Starts the process to download the requested data
		"""

		path = "archive/home/projects/modis/www"
		target = urlparse.urlunsplit((self.scheme, self.netloc, path, '', ''))

		cur_year = datetime.datetime.today().year
		download_list = []

		for grid in self.grids:
			download_list
			tmppath = target + "/" + grid + "/" + self.collection
			print tmppath
			rf = urllib.urlopen(tmppath)
			for line in rf.readlines():
				y = int(self.min_year)
				while y <= cur_year:
					mo = re.search(r">(" + re.escape(str(y)) + r")</a", line)
					if mo and int(mo.group(1)) == y:
						print 'found...'
						download_list.append(mo.group(1))
						break
					y += 1
			rf.close()

			for year in download_list:
				curpath = tmppath + "/" + year
				print 'running===============>', curpath

				tmplog = self.collection + "grid(" + grid + ")-" + year + '.log'
				log = '-o' + tmplog
				p1 = subprocess.Popen(self.cmd + self.opts + [log] + [curpath], stdout=subprocess.PIPE)
				# blocking, based on backgrounded wget process:
				msg = p1.stdout.readline()
				pid = msg.split()[-1][:-1]
				rexp = re.compile(pid + '.*wget')
				while True:
					p2 = subprocess.Popen( ['ps','-A'],stdout=subprocess.PIPE)
					psAout = p2.stdout.read()
					if re.search(rexp,psAout):
						time.sleep(ps_check_interval)
					else:
						break

				print 'done downloading', curpath, ':)'
				print 'moving log file...'

				logpath = self.save_dir+'/logs/'
				print 'logpath = ' + logpath
				try:
					os.makedirs(logpath)
	   			except OSError as exc:
	   				if exc.errno == errno.EEXIST and os.path.isdir(logpath):
	   					pass
	   				else: raise

	   			self.log_loc = logpath+str(datetime.date.today()) + '-' + tmplog
	   			print 'log_loc = ' + self.log_loc
				os.rename(tmplog, self.log_loc)
				print 'log file moved...'

			del download_list[:]
