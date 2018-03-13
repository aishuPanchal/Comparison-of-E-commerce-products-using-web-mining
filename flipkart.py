import bs4
import pymongo
import re
from pymongo import MongoClient
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from pprint import pprint
from threading import Thread



connection = MongoClient()






db = connection["dd"]
collection = db["d"]

def myfunc(text):
	
	search = text.replace(" ","%20")


	my_url ='https://www.flipkart.com/search?q='+search+'&otracker=start&as-show=on&as=off'

	uClient=uReq(my_url)
	page_html=uClient.read()
	uClient.close()

	page_soup=soup(page_html,"html.parser")

	try:
		containers=page_soup.select('div.col._2-gKeQ')
		print(len(containers))
		threadlist = []
		i=0;
		for container in containers:
			i=i+1
			if(i>10):
				break
			try:
			    name = container.findAll("div",{"class":"_3wU53n"})[0].text
			except IndexError:
			    name = 'null'

			try:
			    price = container.findAll("div",{"class":"_1vC4OE _2rQ-NK"})[0].text.strip('₹').strip()
			except IndexError:
			    price = 'null'
			try:
			    rating = container.findAll("div",{"class":"hGSR34 _2beYZw"})[0].text.strip(' ★')
			except IndexError:
			    rating = 'null'
			print("entering..................")
			try:
			    link = container.findAll("a",{"class":"_1UoZlX"})[0]["href"]
			    link = 'https://www.flipkart.com' + link
			    t = Thread(target=parseInfo,args=(link,name,price,rating,))
			    t.start()
			    threadlist.append(t)
			except IndexError:
			    link = 'null'

			print("name : "+name)
			print("price : "+price)
			print("rating : "+rating)
			print("link : "+link)
			print("image : "+image)
			print("*************************")

		for b in threadlist:
			b.join()



			


	except:
		containers='null'

	if not containers:
		try:
			containers=page_soup.select('div.MP_3W3._31eJXZ')
			print(len(containers))
			threadlist1 = []
			i=0
			for container in containers:
				i=i+1
				if(i>10):
					break
				try:
				    name = container.findAll("a",{"class":"_2cLu-l"})[0]["title"]
				except IndexError:
				    name = 'null'
				
				try:
				    price = container.findAll("div",{"class":"_1vC4OE"})[0].text.strip('₹').strip()
				except IndexError:
				    price = 'null'
				try:
				    rating = container.findAll("div",{"class":"hGSR34 _2beYZw"})[0].text.strip(' ★')
				except IndexError:
				    rating = 'null'
				
				print("entering..................")
				try:
				    link = container.findAll("a",{"class":"_2cLu-l"})[0]["href"]
				    link = 'https://www.flipkart.com' + link
				    t = Thread(target=parseInfo,args=(link,name,price,rating,))
				    t.start()
				    threadlist1.append(t)
				except IndexError:
				    link = 'null'



			for b in threadlist1:
				b.join()



		except:
			containers='null'



def parseInfo(link,name,price,rating):

	uClient=uReq(link)
	page_html=uClient.read()
	uClient.close()

	page_soup=soup(page_html,"html.parser")

	try:
		image = page_soup.select('img.sfescn')[0]["src"]

	except IndexError:
		image = 'null'

	collection.insert({
		"buyon" : "flipkart",
		"image" : image,
		"name" : name,
		"price" : price,
		"rating" : rating,
		"link" : link

	})

	print("name : "+name)
	print("price : "+price)
	print("rating : "+rating)
	print("link : "+link)
	print("image : "+image)
	print("*************************")

	




