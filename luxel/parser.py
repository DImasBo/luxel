from bs4 import BeautifulSoup
from bin.offer import Offer
from bin.base import BaseParser

from utils import get_user_agent
from luxel.utils import get_status
from loguru import logger

import requests
import config

# from config import logger_root

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class ClientLuxel(BaseParser):
	site = config.LUXEL_SITE

	def parser_product(self, url):
		r = self.get(url)
		logger.debug(r)
		logger.debug(url)
		
		s = BeautifulSoup(r.text,'html.parser')
		if r.status_code==404:
			logger.error(s.find('h2').text,url)
			return Offer()
		
		offer = Offer(
			title=s.find('h1',{'class':'heading_titleh1'}).getText(),
			url= url, 
			price=s.select_one('.price').getText().replace("₴","").replace('\n',''),
			currency=config.LUXEL_CURRENCY_ID_DEFAULT,
			sku=s.select_one('.code_prod p').getText().replace('Артикул',"").replace(':',""),
			description=str(s.select_one('.tab-content .tab-pane')).replace("\n","").replace("tab-pane",""),
			category=config.LUXEL_CATEGORY_ID_DEFAULT,
			vendor=config.LUXEL_VENDOR
			)
		offer.pictures = [a.get("href") for a in s.select('.flexslider li a')]
		if 0 == len(offer.pictures):
			offer.pictures = [s.select_one('.large-image a').get('href'),]

		for tr in s.select('table.refactor tr'):
			tds = tr.findAll("td")
			if len(tds) == 2: 
				offer.params.append([
					tds[0].getText(),
					tds[1].getText(),
					])
		return offer

class BrowserLuxel():
	"""
	Client selenium browser Firefox site luxel 
	"""
	def __init__(self,**kwargs):
		""" image not download, browser not show """
		profile = webdriver.FirefoxProfile()
		# optimition 
		profile.set_preference("permissions.default.image", 2)
		profile.set_preference("browser.sessionhistory.max_total_viewers", 0)
		profile.set_preference("browser.cache.memory.max_entry_size", 2048)
		profile.set_preference("network.dns.disableIPv6",False)
		profile.set_preference("nglayout.initialpaint.delay",0)
		
		fireFoxOptions = webdriver.FirefoxOptions()
		if kwargs.get('headless',config.HEADLESS_WINDOWS):
			fireFoxOptions.set_headless()
		
		self.drive = webdriver.Firefox(
			executable_path=config.DECKODRIVER_PATH,
			service_log_path=config.DECKODRIVER_LOG_PATH,
			firefox_profile=profile,firefox_options=fireFoxOptions)

	def login(self,email,password):
		self.drive.get(config.LUXEL_LOGIN_LINK)
		self.drive.find_element(By.NAME,"email").send_keys(email)
		self.drive.find_element(By.NAME,"password").send_keys(password + Keys.ENTER)

	def is_login(self):
		self.drive.get(config.LUXEL_LOGIN_LINK)
		if self.drive.current_url == config.LUXEL_LOGIN_IS_LOGIN:
			return True
		return False

	def parser_get_categories(self):
		""" 
		get list all categories with site luxel
		"""
		self.drive.get('https://luxel.ua/index.php?route=optorder/index&pt=aa3b3d90-29e4-11e0-be83-00112f58b61d')
		# open all subcategories
		for subcategory in self.drive.find_elements(By.CSS_SELECTOR,".ttt .catalog-data strong[onclick]"):
			subcategory.click()
		return self.drive.find_elements(By.CSS_SELECTOR, ".ttt .catalog-data ul a")

	def parser_category(self,category):
		"""
		get list data products with table category
		"""
		category.click()
		# wait dowload table 
		offers = []
		try:
			WebDriverWait(self.drive, config.LUXEL_WAIT).until( 
				EC.presence_of_element_located((By.CSS_SELECTOR, "#cat_data table"))
				)
		except TimeoutException:
			logger.error(" not table in "+category.text)
		else:
			# parser table
			self.drive.implicitly_wait(3)

			table_html = self.drive.find_element(By.CSS_SELECTOR, "#cat_data table").get_attribute("outerHTML")
			s = BeautifulSoup(table_html,'html.parser')

			
			if table_html:
				for tr in s.select("tbody tr")[1:]:
					tds = tr.select("td")

					off = Offer(
							title=tds[1].getText().replace("\n",""),
							sku=tds[0].getText().replace("\n",""),
							retai_price=tds[4].getText().replace("грн.","").replace("\n",""),
							retai_price_dns=tds[5].getText().replace("грн.","").replace("\n",""),
							vendor=config.LUXEL_VENDOR
							)

					off.status = get_status( tds[3].getText())
					# chech exits link to product
					off.url = tds[1].select_one("a").get('data-href').replace("\n","") if tds[1].select_one("a") else None
					offers.append(off)
		finally:
			return {
				'title_category':category.text,
				'offers':offers
			}
