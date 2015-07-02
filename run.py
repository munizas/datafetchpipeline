#!/usr/bin/python

def run():
	from retriever.datafetch import FtpFetch, USGSFetch, NERSCFetch
	from validate.wgetlogvalidator import WgetLogValidator
	from utils.emailutils import GmailSend
	
	# setup downloads
	d = FtpFetch("ftp.cdc.noaa.gov", "Datasets/ncep.reanalysis2/gaussian_grid", "shum.2m.gauss.", "/Users/asmuniz/ProjectCode/data/shum", "hdf", "xml", "nc")
	air = FtpFetch("ftp.cdc.noaa.gov", "Datasets/ncep.reanalysis2/gaussian_grid", "air.2m.gauss.", "/Users/asmuniz/ProjectCode/data/air", "hdf", "xml", "nc")
	mintemp = FtpFetch("ftp.cdc.noaa.gov", "Datasets/ncep.reanalysis2.dailyavgs/gaussian_grid", "tmin.2m.gauss.", "/Users/asmuniz/ProjectCode/data/tmin", "hdf", "xml", "nc")
	uwnd = FtpFetch("ftp.cdc.noaa.gov", "Datasets/ncep.reanalysis2/gaussian_grid", "uwnd.10m.gauss.", "/Users/asmuniz/ProjectCode/data/uwnd", "hdf", "xml", "nc")
	
	mod13a1 = USGSFetch('MOLT', 'MOD13A1.005', '/Users/asmuniz/ProjectCode/data/MOD13A1.005', "2015", "hdf", "xml", "nc")
	mod15a2 = USGSFetch('MOLT', 'MOD15A2.005', '/Users/asmuniz/ProjectCode/data/MOD15A2.005', "2015", "hdf", "xml", "nc")
	mcd43b2 = USGSFetch('MOTA', 'MCD43B2.005', '/Users/asmuniz/ProjectCode/data/MCD43B2.005', "2015", "hdf", "xml", "nc")
	mcd43b3 = USGSFetch('MOTA', 'MCD43B3.005', '/Users/asmuniz/ProjectCode/data/MCD43B3.005', "2015", "hdf", "xml", "nc")
	mcd12q1 = USGSFetch('MOTA', 'MCD12Q1.051', '/Users/asmuniz/ProjectCode/data/MCD12Q1.051', "2012", "hdf", "xml", "nc")

	mod04_l2 = NERSCFetch('MOD04_L2', '/Users/asmuniz/ProjectCode/data/MOD04_L2', "2013", "tar")
	mod05_l2 = NERSCFetch('MOD05_L2', '/Users/asmuniz/ProjectCode/data/MOD05_L2', "2013", "tar")
	mod06_l2 = NERSCFetch('MOD06_L2', '/Users/asmuniz/ProjectCode/data/MOD06_L2', "2013", "tar")
	mod07_l2 = NERSCFetch('MOD07_L2', '/Users/asmuniz/ProjectCode/data/MOD07_L2', "2013", "tar")
	mod11_l2 = NERSCFetch('MOD11_L2', '/Users/asmuniz/ProjectCode/data/MOD11_L2', "2013", "tar")

	# perform download operation
	d.fetch()
	air.fetch()
	mintemp.fetch()
	uwnd.fetch()
	mod13a1.fetch()
	mod15a2.fetch()
	mcd43b2.fetch()
	mcd43b3.fetch()
	mod04_l2.fetch()
	mod05_l2.fetch()
	mod06_l2.fetch()
	mcd12q1.fetch()
	
	# validate wget logs
	logV = WgetLogValidator()
	logV.validate_logs(d.log_loc, air.log_loc, mintemp.log_loc, uwnd.log_loc, mod13a1.log_loc, mod15a2.log_loc, mcd43b2.log_loc, mcd43b3.log_loc, mcd12q1.log_loc, mod04_l2.log_loc, mod05_l2.log_loc, mod06_l2.log_loc, mod07_l2.log_loc, mod11_l2.log_loc) # append log files
	
	#set up email
	credfile = open("/Users/asmuniz/Desktop/emailcred.txt", 'r')
	login_user = credfile.readline().rstrip('\n')
	user_pwd = credfile.readline().rstrip('\n')
	credfile.close()
	from_user = login_user

	to_users = []
	emailfile = open("/Users/asmuniz/Desktop/emails.txt", 'r')
	for email in emailfile:
		to_users.append(email.rstrip('\n'))
	emailfile.close()
	subject = 'Daily Download Summary'
	text = logV.summary_str()

	mailObj = GmailSend(login_user, user_pwd, from_user, subject, text, to_users)
	mailObj.send_email()
	
	
if __name__ == "__main__":
	run()