# -*- coding: utf-8 -*-
import requests
import config

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
	
def chunks(l, n):
	for i in range(0, len(l), n):
		yield l[i:i + n]