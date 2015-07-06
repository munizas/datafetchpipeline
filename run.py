#!/usr/bin/python

def run():
	from retriever.datafetch import FtpFetch, USGSFetch, NERSCFetch
	from validate.wgetlogvalidator import WgetLogValidator
	from utils.emailutils import GmailSend
	from config.config import Config
	import json

	config = Config()
	f = open(config.datapath(), "r")
	jsonobj = json.loads(f.read())
	f.close()

	# queue up fetch objects
	fetch_list = []
	for obj in jsonobj['ftp']:
		fetch_list.append(FtpFetch(obj['site'], obj['collection'], obj['file_name_root'], obj['save_dir'], obj['exts']))

	for obj in jsonobj['usgs']:
		fetch_list.append(USGSFetch(obj['modis_terra'], obj['collection'], obj['save_dir'], obj['min_year'], obj['exts']))

	for obj in jsonobj['nersc']:
		fetch_list.append(NERSCFetch(obj['collection'], obj['save_dir'], obj['min_year'], obj['exts']))

	#fetch
	logs = []
	for fobj in fetch_list:
		fobj.fetch()
		logs.append(fobj.log_loc)

	#validate logs
	logV = WgetLogValidator()
	logV.validate_logs(logs)
	
	subject = 'Daily Download Summary'
	text = logV.summary_str()
	
	mailObj = GmailSend(config.emailusr(), config.emailpwd(), config.emailusr(), subject, text, config.emaillist())
	mailObj.send_email()
	
if __name__ == "__main__":
	run()