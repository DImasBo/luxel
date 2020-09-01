# from luxel.parser import AdapterLuxel, LuxelParser
from luxel.adapter import Luxel

from datetime import datetime
from multiprocessing import Pool
import logging
import config
from config import logger_root
import os	
import csv
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser( add_help=False)
	parser.add_argument("site", help="which version of the parser to run?")
	parser.add_argument("type", help="1 = short product parsing, 2 = details product parsing")
	
	args = parser.parse_args()
	logger_root.info(args)
	
	if args.site == 'luxel':
		luxel = Luxel()
		if args.type == "1":
			logger_root.info("Start short product parsing Luxel")
			luxel.parser_short_prdouct()
		elif args.type == "2":
			logger_root.info("Start details product parsing Luxel")
			luxel.parser_details_prdouct()