from luxel.parser import AdapterLuxel, LuxelParser
import config

def test_adapter():
	a = AdapterLuxel()
	a.login(config.LUXEL_LOGIN,config.LUXEL_PASSWORD)	
	categories = a.parser_get_categories()
	a.parser_category(categories[0])
test_adapter()