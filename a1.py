from flask import Flask, render_template, request
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import flipkart
import amazon
import ebay
from amazon import *
from ebay import *
from flipkart import *


app = Flask(__name__)

@app.route('/send',methods=['GET','POST'])
def index():
	print("callng index")
	i=0
	add = 0
	maxv = 0
	dic={}
	if request.method == 'POST':
		text = request.form['search']
		key = text

		print("printing db from another file*****************************************************")

		cursor = collection.find({"name": {"$regex": key, "$options": "i"}})
		print(cursor.count())
		if(cursor.count()>0):
			
			for document in cursor:
				
				print("###################################### printing from database #############################################")
				pprint(document)
				title = document["name"]
				image = document["image"]
				price = document["price"]
				rating = document["rating"]
				buyon = document["buyon"]
				link = document["link"]

				new_pr = price.replace(",","")
				print(new_pr)

				if price == 'null':
					print ('working')
					new_pr = '0.0';


				print(float(new_pr))

				add = add + float(new_pr)
				if(float(new_pr) > maxv):
					maxv = float(new_pr)

				

			avg = add/cursor.count()
			print("+++++++++++++++++++++++++++++++++++++++++++++++++++==")
			print(avg)
			print(cursor.count())

			cursor = collection.find({"name": {"$regex": key, "$options": "i"}})
			tu=[]

			for document in cursor:
				i=i+1
				print("###################################### printing from new_value #############################################")
				pprint(document)

				title = document["name"]
				image = document["image"]
				price = document["price"]
				rating = document["rating"]
				buyon = document["buyon"]
				link = document["link"]
				new_pr = price.replace(",","")

				if rating == 'null':
					ratt = 0
				else:
					rat = rating.replace(" out of 5 stars","")
					ratt = float(rat)
				if  new_pr == 'null':
					new_pr = '0.0';
				np = float(new_pr)

				if(np<=avg):
					continue

				if(ratt > 3):
					tu.append((np,title,image,rating,buyon,link))


				sorted(tu)
				print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
				print(tu)

				for j in tu:
					dic.update({'amazon'+str(i):{
						'title':j[1],
						'img':j[2],
						'link_url' : j[5],
						'price': j[0],
						'rating': j[3],
						'buyon' : j[4]

					}})


		

		else:
			amazon.myfunc(text)
			flipkart.myfunc(text)
			ebay.myfunc(text)
			dic={}
			print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! we crawled first !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			cursor = collection.find({"name": {"$regex": key, "$options": "i"}})
			print(cursor.count())
			for document in cursor:
				pprint(document)
				title = document["name"]
				image = document["image"]
				price = document["price"]
				rating = document["rating"]
				buyon = document["buyon"]
				link = document["link"]



				new_pr = price.replace(",","")
				print(new_pr)

				if price == 'null':
					print ('working')
					new_pr = '0.0';
				
				
				print(float(new_pr))

				add = add + float(new_pr)
				if(float(new_pr) > maxv):
					maxv = float(new_pr)

				

			avg = add/cursor.count()
			print("+++++++++++++++++++++++++++++++++++++++++++++++++++==")
			print(avg)
			print(cursor.count())

			cursor = collection.find({"name": {"$regex": key, "$options": "i"}})
			tu=[]

			for document in cursor:
				i=i+1
				print("###################################### printing from new_value #############################################")
				pprint(document)

				title = document["name"]
				image = document["image"]
				price = document["price"]
				rating = document["rating"]
				buyon = document["buyon"]
				link = document["link"]
				new_pr = price.replace(",","")

				if rating == 'null':
					ratt = 0
				else:
					rat = rating.replace(" out of 5 stars","")
					ratt = float(rat)
				if  new_pr == 'null':
					new_pr = '0.0';
				np = float(new_pr)

				if(np <= avg):
					continue

				if(ratt > 3):
					
					dic.update({'amazon'+str(i):{
						'title':j[1],
						'img':j[2],
						'link_url' : j[5],
						'price': j[0],
						'rating': j[3],
						'buyon' : j[4]

					}})






		#print(dic)


		
				

		
		



		
		return render_template('result.html',name=dic)

	return render_template('index.html')

if __name__ == "__main__":
	app.run()