import requests
import config

from utils import get_user_agent

class BaseParser:
	"""
	Базовий клас для парсеров 
	"""
	headers = {}
	category_link_list = None
	site = None

	def set_user_agent(self):
		self.headers['User-Agent'] = get_user_agent(self.site)		

	def __init__(self, *args, **kwargs):
		self.set_user_agent()

	def get(self,url):
		r = requests.get(url, headers=self.headers)
		print(r, self.headers, url)
		if r.status_code == 200:
			return r
		elif r.status_code==403:
			self.set_user_agent()
			return self.get(url)
		print("ERRORR REQUESTS!!!!")
		print(r, url,self.headers)
		return r

	def parser_categories_link(self, url, limit=100):
		"""
			return {
			'title_category':title_category,
			'product_link_list':offers,
			'page_count':page_count
			}
		"""
		pass

	def parser_product(self, url):
		"""
		return object Offer 
		"""
		pass
