from .parser import BrowserLuxel, ClientLuxel
from datetime import datetime
from utils import formater_csv_write
import os
import config
import csv
from selenium.common.exceptions import StaleElementReferenceException
from multiprocessing import Pool
# from utils import CSV_1c
FORMAT_FOLDER_RESULT = "%Y-%m-%d"

class Luxel:
	

	def __init__(self, **kwargs):
		self.result_dir = "luxel/result/"+datetime.today().strftime(FORMAT_FOLDER_RESULT)
		if not os.path.isdir(self.result_dir):
			os.mkdir(self.result_dir)
		self.file_name = self.result_dir+'/result_short.csv'
		self.flows = kwargs.get('flows', config.LUXEL_FLOWS)
		self.count_pool = kwargs.get('count_pool', config.LUXEL_COUNT_POOL)
		self.login = kwargs.get('count_pool', config.LUXEL_LOGIN)
		self.passwd = kwargs.get('count_pool', config.LUXEL_PASSWORD)
		# self.csv_1c = CSV_1c
	def parser_short_prdouct(self):		
		'''
		збір данних про товари з коротким описом
		'''
		aLuxel = BrowserLuxel()

		aLuxel.login(self.login, self.passwd)

		# parser коротку информацию о товаре
		i = 0
		flag_dom = True

		while self.count_pool > i and flag_dom:
			try:
				with open(self.file_name,"w") as f:
					writer = csv.writer(f,delimiter=config.DELLIMITED)
					writer.writerow(['url','title','sku','Сategory Luxel','status','Price without VAT','Price with VAT'])
				categories = aLuxel.parser_get_categories()
				for category in categories:
					data_category = aLuxel.parser_category(category)
					print("%s products count %d" % ( data_category['title_category'], len(data_category['offers'])) )

					with open(self.file_name,"a") as f:
						writer = csv.writer(f,delimiter=config.DELLIMITED)
						data = [[
									formater_csv_write(offer.url),
									formater_csv_write(offer.title),
									formater_csv_write(offer.sku).replace(" ",""),
									formater_csv_write(data_category['title_category']),
									formater_csv_write(offer.status),
									formater_csv_write(offer.retai_price),
									formater_csv_write(offer.retai_price_dns),
									] for offer in data_category['offers']
								]	
						writer.writerows(data)
				flag_dom = False
			except StaleElementReferenceException:
				print("%d: ERROR: %s" % (i, StaleElementReferenceException))
			except Exception as e:
				print("%d: ERROR: %s" % (i, e))
			i += 1
			
		aLuxel.drive.close()
		aLuxel.drive.quit()

	def map_details_product(self, data):
		
		with open(self.luxel_result_file,'a') as f:
			writer = csv.writer(f,delimiter=config.DELLIMITED)
			if data.get('url'):
				offer = ClientLuxel().parser_product(data['url'])	
				writer.writerow([data['url'],data['title'],data['sku'],data['Сategory Luxel'],data['status'],data['Price without VAT'],data['Price with VAT'],
					offer.price,
					"^".join([p[0]+"="+p[1] for p in offer.params]),
					" ".join(offer.pictures),
					])
			else:
				writer.writerow([data['url'],data['title'],data['sku'],data['Сategory Luxel'],data['status'],data['Price without VAT'],data['Price with VAT']])


	def parser_details_prdouct(self):
		'''
		збір данних про товари з детальним описом описом
		'''

		self.parser_short_prdouct()
		data_short = []
		with open(self.file_name) as f:
			data_short = [item for item  in csv.DictReader(f,delimiter=config.DELLIMITED)]

		self.luxel_result_file = self.file_name.replace('result_short','result_detail')

		with open(self.luxel_result_file,'w') as f:
			writer = csv.writer(f,delimiter=config.DELLIMITED)
			writer.writerow(['url','title','sku','Сategory Luxel','status','Price without VAT','Price with VAT','price','params','pictures'])

		with Pool(self.flows) as p:
			p.map(self.map_details_product, data_short)
    