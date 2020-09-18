from .parser import BrowserLuxel, ClientLuxel
from loguru import logger
from datetime import datetime
from utils import formater_csv_write, chunks
import os
import config
import csv
from selenium.common.exceptions import StaleElementReferenceException
from multiprocessing import Pool

FORMAT_FOLDER_RESULT = "%Y-%m-%d"

class Luxel:
	

	def __init__(self, **kwargs):
		self.result_dir = config.LIXEL_DIRECTORY_RESULT+datetime.today().strftime(FORMAT_FOLDER_RESULT)
		logger.debug(os.path.isdir(self.result_dir))
		logger.debug(self.result_dir)
		if not os.path.isdir(self.result_dir):
			os.mkdir(self.result_dir)
		self.file_name = self.result_dir+'/result_short.csv'
		self.file_name_buk = self.result_dir+'/result_buk.txt'
		self.flows = kwargs.get('flows', config.LUXEL_FLOWS)
		self.count_pool = kwargs.get('count_pool', config.LUXEL_COUNT_POOL)
		self.login = kwargs.get('count_pool', config.LUXEL_LOGIN)
		self.passwd = kwargs.get('count_pool', config.LUXEL_PASSWORD)
		# with open(self.file_name_buk,"w") as f:
			# pass

	def parser_short_prdouct(self):		
		'''
		збір данних про товари з коротким описом
		'''
		aLuxel = BrowserLuxel()
		# parser коротку информацию о товаре
		i = 0
		flag_dom = False
		aLuxel.login(self.login, self.passwd)
		logger.info("open browser and login " + self.login)

		if aLuxel.is_login:
			order_log = ""
			order_count = 0
			while self.count_pool > i and not flag_dom:
				try:
					with open(self.file_name,"w") as f:
						writer = csv.writer(f,delimiter=config.DELLIMITED)
						writer.writerow(['url','title','sku','category','status','vendor','price VAT'])
					categories = aLuxel.parser_get_categories()
					for category in categories:
						data_category = aLuxel.parser_category(category)
						# log order
						order_count+=len(data_category['offers'])
						logger.debug("%s products count %d" % ( data_category['title_category'], len(data_category['offers'])) )

						with open(self.file_name,"a") as f:
							writer = csv.writer(f,delimiter=config.DELLIMITED)
							data = [[
										formater_csv_write(offer.url),
										formater_csv_write(offer.title),
										formater_csv_write(offer.sku).replace(" ",""),
										formater_csv_write(data_category['title_category']),
										formater_csv_write(offer.status),

										formater_csv_write(offer.vendor),
										formater_csv_write(offer.retai_price),
										formater_csv_write(offer.retai_price_dns),
										] for offer in data_category['offers']
									]	
							writer.writerows(data)
					flag_dom = False
				
				except Exception as e:
					logger.error(e)
				finally:
					logger.info(" | ".join([category.text for category in categories]))
					logger.info("count products %d" % (order_count,))
					i += 1
					if order_count > 0	:
						flag_dom = True
		aLuxel.drive.close()
		aLuxel.drive.quit()

		logger.info("close browser")

	def map_details_product(self, data):
		import time
		with open(self.luxel_result_file,'a') as f:
			writer = csv.writer(f,delimiter=config.DELLIMITED)
			if data.get('url'):
				offer = ClientLuxel().parser_product(data['url'])	
				writer.writerow([data['url'],data['title'],data['sku'],data['category'],data['status'],data['vendor'],data['price VAT'],
					offer.price,
					"^".join([p[0]+"="+p[1] for p in offer.params]),
					" ".join(offer.pictures),
					offer.description
					])
				offer.info()
			else:
				writer.writerow([data['url'],data['title'],data['sku'],data['category'],data['status'],data['vendor'],data['price VAT']])
		time.sleep(config.LUXEL_SLEEP)

	def parser_details_prdouct(self):
		'''
		збір данних про товари з детальним описом описом
		'''
		# file_name_buk
		
		data_short = []
		with open(self.file_name) as f:
			data_short = [item for item  in csv.DictReader(f,delimiter=config.DELLIMITED)]
				
		self.luxel_result_file = self.file_name.replace('result_short','result_detail')

		with open(self.luxel_result_file,'w') as f:
			writer = csv.writer(f,delimiter=config.DELLIMITED)
			writer.writerow(['url','title','sku','сategory','status','vendor','Price VAT','price','params','pictures','description'])


		for data in list(chunks(list(filter( config.LUXEL_FILTER_LAMBDA, data_short)),150)):
			with Pool(self.flows) as p:
				p.map(self.map_details_product, data)
		# sorted
		data_sort = []
		with open(self.luxel_result_file,'r') as f:
			reader = [item for item  in csv.DictReader(f,delimiter=config.DELLIMITED)]
			data_sort = sorted(reader, key=lambda data: data['сategory'], reverse=False )

		with open(self.luxel_result_file,'w') as f:
			writer = csv.DictWriter(f,delimiter=config.DELLIMITED,fieldnames=['url','title','sku','сategory','status','vendor','description','Price VAT','price','params','pictures'])
			writer.writeheader()
			for vals in data_sort:
				writer.writerow(vals)
