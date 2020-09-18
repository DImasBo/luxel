# from luxel.parser import AdapterLuxel, LuxelParser
from luxel.adapter import Luxel

from datetime import datetime
from multiprocessing import Pool
import logging
import config
import os	
import csv
import argparse

def while_poll(func):
	""" 
	зачиклить якщо парсер видасть помилку
	"""
	def wrapper():
		flag_dom = True
		i=0
		while config.LUXEL_COUNT_POOL > i and flag_dom:
			try:
				func()
				flag_dom = False
			except Exception as e:
				print("Erorr: %s" %(e,))
			finally:
				i += 1
				print("parser finally")
	return wrapper

@while_poll
def parsing_dashboard():
	print("Start short product parsing Luxel")
	luxel.parser_short_prdouct()

@while_poll
def parsing_details():
	print("Start details product parsing Luxel")
	luxel.parser_details_prdouct()

if __name__ == '__main__':
	parser = argparse.ArgumentParser( add_help=False)
	parser.add_argument("site", help="which version of the parser to run?")
	parser.add_argument("type", help="1 = short product parsing, 2 = details product parsing")
	
	args = parser.parse_args()
	print(args)
	
	if args.site == 'luxel':
		luxel = Luxel()
		if args.type == "1":
			parsing_dashboard()
		elif args.type == "2":
			parsing_details()
		elif args.type == "3":
			parsing_dashboard()
			parsing_details()