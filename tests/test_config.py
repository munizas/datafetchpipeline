from ..config.config import Config
import re
from datetime import date

def test_values():
	c = Config()
	assert c.datapath() == '/Users/asmuniz/ProjectCode/datapipeline/config/data.json'
	assert c.emailusr() == 'jpldatabot@gmail.com'
	assert c.emaillist() == ['gus.s.muniz@gmail.com', 'agustin.s.muniz@jpl.nasa.gov', 'solkim1@gmail.com', 'tjmcdonald@ucla.edu']
	assert c.convertlistpath() == '/Users/asmuniz/ProjectCode/datapipeline/filetrack/'
	assert c.preconwatch() == ['MOD06_L2']
	assert re.search(c.redataproduct(), '/Users/asmuniz/ProjectCode/data/MOD04_L2/logs/2015-06-30-MOD04_L2grid(240)-2013.log').group(1) == 'MOD04_L2'
	assert c.preconfilename() == c.convertlistpath() + str(date.today()) + '-preconlist.txt'
	assert c.wgetpath() == '/usr/local/bin/wget'