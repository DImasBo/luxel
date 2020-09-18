from luxel.parser import ClientLuxel
import config

# def test_adapter():
# 	a = AdapterLuxel()
# 	a.login(config.LUXEL_LOGIN,config.LUXEL_PASSWORD)	
# 	categories = a.parser_get_categories()
# 	a.parser_category(categories[0])
# test_adapter()

def test_parser_product():
	url  = 'https://luxel.ua/svetodiodnoe--led--osveshhenie/led-ulichnie-svetilniki/ulichnij-svetilnik-lxsl-100c'
	luxel = ClientLuxel()
	product = luxel.parser_product(url)
	print(product.title)
	print(product.description)
test_parser_product()

# def test_adapter():
# 	a = AdapterLuxel()
# 	a.login(config.LUXEL_LOGIN,config.LUXEL_PASSWORD)	
# 	categories = a.parser_get_categories()
# 	a.parser_category(categories[0])
# test_adapter()