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

		my_url =my_url ='https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords='+search
		search_ebay = search.replace(" ","+")
		my_url_ebay ='https://www.ebay.in/sch/i.html?_nkw='+search
		uClient=uReq(my_url)
		page_html=uClient.read()
		uClient.close()
		print("amazon passed")
		uClient=uReq(my_url_ebay)
		print("ebay requested")
		page_html1=uClient.read()
		print("reading ebay complete")
		uClient.close()
		print("ebay passed")


		page_soup=soup(page_html,"html.parser")
		page_soup1 = soup(page_html1,"html.parser")
		containers=page_soup.findAll("div",{"class":"s-item-container"})
		
		#print(len(containers))
		dic ={}
		dict2={}
		dict3={}
		i=0
		
		for container in containers:
			i=i+1
			if i>5:
				break
			else:
				contain = container.findAll("div",{"class":"a-fixed-left-grid-col a-col-right"})[0]
				imgsrc = container.findAll("div",{"class":"a-fixed-left-grid-col a-col-left"})[0]
				

				dic.update({'amazon'+str(i):{
					'title':contain.div.div.a["title"],
					'img':imgsrc.div.div.a.img["src"],
					'link_url' : contain.div.div.a["href"],
					'price':contain.findAll("span",{"class":"a-size-base a-color-price s-price a-text-bold"})[0].text.strip(),
					'rating': contain.findAll("span",{"class":"a-declarative"})[0].a.i.text
					

					}})
		
		i=0		
		
		containers=page_soup1.findAll("li",{"class":"sresult lvresult clearfix li shic"})
		for container in containers:
			i=i+1
			if i>5:
				break
			else:
				dic.update({'ebay'+str(i):{
					'title':container.findAll("h3",{"class":"lvtitle"})[0].a.text,
					'img':container.findAll("div",{"class":"lvpic pic img left"})[0].div.a.img["src"],
					'link_url' : container.findAll("div",{"class":"lvpic pic img left"})[0].div.a["href"],
					'price':container.findAll("li",{"class":"lvprice prc"})[0].text.strip(),
					'rating':'not available'
					

					}})


		print(dic)
		#dict3 = dict.copy()
		#dict3.update(dict2)


		
		return render_template('result.html',name=dic)

	return render_template('index.html')

if __name__ == "__main__":
	app.run()