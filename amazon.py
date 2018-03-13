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
	
	my_url ='https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords='+search

	uClient=uReq(my_url)
	page_html=uClient.read()
	uClient.close()

	page_soup=soup(page_html,"html.parser")

	containers=page_soup.select('ul#s-results-list-atf > li > div.s-item-container')
	print(len(containers))

	i=0;
	threadlist = []

	for container in containers:
		i=i+1;
		if i>10 :
			break
			#cursor = collection.find({})
			#for document in cursor:
				#pprint(document)

			#break
		
		try:
		    link_url = container.select('a.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal')[0]["href"]
		    pr = container.select('span.a-size-base.a-color-price.s-price.a-text-bold')[0].text.strip()
		    rat = container.select('i > span.a-icon-alt')[0].text
		    #parseInfo(link_url)
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
	    image = page_soup1.findAll("div",{"class":"imgTagWrapper"})[0].img["src"]
	except IndexError:
	    image = 'null'

	try:
	    name = page_soup1.findAll("span",{"id":"productTitle"})[0].text.strip()
	except IndexError:
	    name = 'null'

	try:
	    price = page_soup1.findAll("span",{"id":"priceblock_ourprice"})[0].text.strip()
	except IndexError:
		price = pr

	try:
	    rating = page_soup1.findAll("span",{"id":"acrPopover"})[0]["title"]
	except IndexError:
		rating = rat

	collection.insert({
		"buyon" : "amazon",
		"image" : image,
		"name" : name,
		"price" : price,
		"rating" : rating,
		"link" : link

		})



		

		


			
			