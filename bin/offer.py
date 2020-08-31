import config

class Offer:

	def __init__(self,*args,**kwargs):
		self.title = kwargs.get('title')
		self.url = kwargs.get('url')
		self.price = kwargs.get('price', 0)
		self.retai_price = kwargs.get('retai_price', 0)
		self.retai_price_dns = kwargs.get('retai_price_dns', 0)
		
		self.currency = kwargs.get('currency')
		self.sku = kwargs.get('sku')
		self.description = kwargs.get('description')
		self.params = kwargs.get('params',[])
		self.status = kwargs.get('status')
		self.category = kwargs.get('category')
		self.pictures = kwargs.get('pictures',[])
		self.vendor = kwargs.get('vendor')

		# self.info()

	def info(self):
		print("========= %s =======" % (self.title,))
		print(self.url)
		print(self.sku)

	def get_data():
		return {
			"title":self.title,
			"description":self.description,
			"url":self.url,
			"sku":self.sku,
			"pictures":self.pictures,
			"currency":self.currency,
			"params":self.params,
			"status":self.status,
			"category":self.category,
			"vendor":self.vendor,
		}