import bs4
import pymongo
import re
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from pymongo import MongoClient
from pprint import pprint
from threading import Thread

connection = MongoClient()

db = connection["dd"]
collection = db["d"]

dic = {}
pr='null'
rat='null'

def myfunc(text):
	search = text.replace(" ","+")
	my_url ='https://www.ebay.in/sch/i.html?_nkw='+search.replace(" ","+")

	uClient=uReq(my_url)
	page_html=uClient.read()
	uClient.close()

	page_soup=soup(page_html,"html.parser")
	containers=page_soup.select('li.sresult.lvresult.clearfix.li.shic')
	print(len(containers))

	i=0
	threadlist = []

	for container in containers:
		i=i+1
		if i>10:
			break
		try:
			link_url = container.select('h3.lvtitle > a')[0]["href"]
			price = container.select('li.lvprice.prc')[0].text.strip()
			t = Thread(target=parseInfo,args=(link_url,))
			t.start()
			threadlist.append(t)

		except IndexError:
			link_url = 'null'

	for b in threadlist:
		b.join()

def parseInfo(link):
	print("parseInfo called")
	print(link)
	uClient1=uReq(link)
	page_html1=uClient1.read()
	uClient1.close()
	page_soup1=soup(page_html1,"html.parser")

	try:
		image = page_soup1.select('div#PicturePanel')[0].select('img#icImg')[0]["src"]

	except IndexError:
		image = 'null'
	try:
		name = page_soup1.select('h1#itemTitle')[0].text.strip('Details about  \xa0')
	except IndexError:
		name='null'
	try:
		price = page_soup1.select('span#prcIsum')[0].text.strip("Rs.").strip(" ")
	except IndexError:
		price='null'
	print(image)
	print(name)
	print(price)
	print(link)
	print("##########################################################################")

	collection.insert({
		"buyon" : "ebay",
		"image" : image,
		"name" : name,
		"price" : price,
		"rating" : "0.0",
		"link" : link

	})

		






