import config

def get_status(status):
	for luxel, region in config.LUXEL_STATUS.items():
		if luxel in status:
			return region
	return status