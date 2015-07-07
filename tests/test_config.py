from ..config.config import Config

def test_values():
	c = Config()
	assert c.datapath() == '/Users/asmuniz/ProjectCode/datapipeline/config/data.json'
	assert c.emailusr() == 'jpldatabot@gmail.com'
	assert c.emailpwd() == 'Jpldatab0t'
	assert c.emaillist() == ['gus.s.muniz@gmail.com', 'agustin.s.muniz@jpl.nasa.gov', 'solkim1@gmail.com', 'tjmcdonald@ucla.edu']