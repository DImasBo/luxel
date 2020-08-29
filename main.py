# from luxel.parser import AdapterLuxel, LuxelParser
from luxel.adapter import Luxel

from datetime import datetime
from multiprocessing import Pool

import config
import os	
import csv
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser( add_help=False)
	parser.add_argument("site", help="which version of the parser to run?")
	parser.add_argument("type", help="1 = short product parsing, 2 = details product parsing")
	
	args = parser.parse_args()
	print(args)
	
	if args.site == 'luxel':
		luxel = Luxel()
		if args.type=='1':
			print("Start short product parsing Luxel")
			luxel.parser_short_prdouct()
		elif args.type=='2':
			print("Start details product parsing Luxel")
			luxel.parser_details_prdouct()