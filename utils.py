# -*- coding: utf-8 -*-
import requests
import config
import csv

def get_user_agent(url, headers={}):
	list_user_agent = []
	with open(config.USER_AGENT_FILE) as f:
		list_user_agent = f.read().split("\n")

	for user_agent in list_user_agent:
		headers['User-Agent'] = user_agent
		r = requests.get(url,headers=headers)
		if r.status_code==200:
			return user_agent

def formater_csv_write(text):
	if text:
		return str(text).replace("\t"," ").replace("\n"," ").replace("  "," ")
	return ""

class CSV_1c:
	
	def __init__(self, file_name, **kwargs):
		self.file_name = file_name

		with open(self.file_name,"w") as f:
			writer = csv.writer(f,delimiter=config.DELLIMITED) 
			writer.writerow(['url','title','sku','category','status','price','params','pictures'])

	def writerow(self, data):
		with open(self.file_name,"a") as f:
			writer = csv.writer(f,delimiter=config.DELLIMITED) 
			writer.writerow(data)
