import pickle

def writeReleaseToPickle(release, fileName):
	"""Pickles the release data."""

	with open(fileName, 'wb') as f:
		pickle.dump(release, f)
	

def getReleaseFromPickle(fileName):
	"""Reads a release info from a pickle file."""

	with open(fileName, 'rb') as f:
		releasePickle = pickle.load(f)
	release = releasePickle['release']

	return release


