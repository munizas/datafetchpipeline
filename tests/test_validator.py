from ..validate.wgetlogvalidator import WgetLogValidator

def test():
	v = WgetLogValidator()
	logs = ['/Users/asmuniz/ProjectCode/data/air/logs/2015-06-19-air.2m.gauss.log', '/Users/asmuniz/ProjectCode/data/MOD04_L2/logs/2015-06-30-MOD04_L2grid(240)-2013.log', '/Users/asmuniz/ProjectCode/data/MCD12Q1.051/logs/2015-07-03-2012.01.01.log', '/Users/asmuniz/Desktop/develop/project-info/gregg_data_processing/success.log', '/Users/asmuniz/Desktop/develop/project-info/gregg_data_processing/no-re-retrieve.log', '/Users/asmuniz/Desktop/develop/project-info/gregg_data_processing/network-error.log']
	v.validate_logs(logs)
	print v.summary_str()