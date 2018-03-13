from flask import Flask, render_template, request
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


app = Flask(__name__)

@app.route('/send',methods=['GET','POST'])
def index():
	print("callng index")
	if request.method == 'POST':
		search = request.form['search']
		key = search
		a_search = search.replace(" ","+")
		my_url ='https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords='+a_search
		
		uClient=uReq(my_url)
		page_html=uClient.read()
		uClient.close()

		print("amazon passed")

		
		
		
		


		page_soup=soup(page_html,"html.parser")
		
		containers=page_soup.findAll("div",{"class":"s-item-container"})
		
		dic ={}
		
		i=0
		
		for container in containers:
			i=i+1
			if i>3:
				break
			else:
				contain = container.findAll("div",{"class":"a-fixed-left-grid-col a-col-right"})[0]
				imgsrc = container.findAll("div",{"class":"a-fixed-left-grid-col a-col-left"})[0]
				

				dic.update({'amazon'+str(i):{
					'title':contain.div.div.a["title"],
					'img':imgsrc.div.div.a.img["src"],
					'link_url' : contain.div.div.a["href"],
					'price':contain.findAll("span",{"class":"a-size-base a-color-price s-price a-text-bold"})[0].text.strip(),
					'rating': contain.findAll("span",{"class":"a-declarative"})[0].a.i.text,
					'buyon' : 'amazon'

					}})
		
		#search = search.replace(" ","+")
		my_url ='https://www.ebay.in/sch/i.html?_nkw='+search.replace(" ","+")
		uClient=uReq(my_url)
		page_html=uClient.read()
		uClient.close()
		print("reading ebay complete")
		
		print("ebay passed")


		page_soup=soup(page_html,"html.parser")
		containers=page_soup.findAll("li",{"class":"sresult lvresult clearfix li shic"})
		#print(len(containers))
		
		i=0
		for container in containers:
			i=i+1
			if i>3:
				break
			else:
							

				dic.update({'ebay'+str(i):{
					'title':container.findAll("h3",{"class":"lvtitle"})[0].a.text,
					'img':container.findAll("div",{"class":"lvpic pic img left"})[0].div.a.img["src"],
					'link_url' : container.findAll("div",{"class":"lvpic pic img left"})[0].div.a["href"],
					'price':container.findAll("li",{"class":"lvprice prc"})[0].text.strip(),
					'rating': 'no rating',
					'buyon' : 'ebay'

					}})

		my_url ='https://www.snapdeal.com/search?keyword='+search.replace(' ','%20')+'&sort=rlvncy'
		uClient=uReq(my_url)
		
		page_html=uClient.read()
		
		
		uClient.close()
		print("snapdeal passed")


		page_soup=soup(page_html,"html.parser")
		containers=page_soup.findAll("div",{"class":"product-tuple-description "})
		imgsrc=page_soup.findAll("div",{"class":"product-tuple-image "})
		#print(len(containers))
		dict ={}
		i=0
		for container in containers:
			i=i+1
			if i>3:
				break
			else:
				#contain = container.findAll("div",{"class":"product-tuple-description "})[0]
				#imgsrc = container.findAll("div",{"class":"a-fixed-left-grid-col a-col-left"})[0]
				

				dic.update({'snapdeal'+str(i):{
					'title':container.div.a.p["title"],
					'img':imgsrc[i].a.picture.img["src"],
					'link_url' : container.div.a["href"],
					'price':container.findAll("span",{"class":"lfloat product-price"})[0].text.strip(),
					'rating': 'no rating',
					'buyon' : 'snapdeal'

					}})


		print(dic)
		#dict3 = dict.copy()
		#dict3.update(dict2)


		
		return render_template('result.html',name=dic)

	return render_template('index.html')

if __name__ == "__main__":
	app.run()