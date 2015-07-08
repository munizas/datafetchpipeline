from ..retriever.datafetch import FtpFetch

def test_params():
	scheme = 'ftp'
	netloc = 'ftp.cdc.noaa.gov'
	collection = 'Datasets/ncep.reanalysis2/gaussian_grid'
	file_name_root = 'shum.2m.gauss.'
	save_dir = '/Users/asmuniz/ProjectCode/data/shum'
	
	d = FtpFetch(netloc, collection, file_name_root, save_dir, ["hdf", "xml", "nc"])

	assert d.scheme == scheme
	assert d.netloc == netloc
	assert d.collection == collection
	assert d.file_name_root == file_name_root
	assert d.save_dir == save_dir