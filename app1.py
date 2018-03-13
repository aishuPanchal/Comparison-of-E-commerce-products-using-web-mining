from flask import Flask, render_template, request
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


app = Flask(__name__)

@app.route('/send',methods=['GET','POST'])
def index():
	if request.method == 'POST':
		search = request.form['search']
		search = search.replace(" ","+")
		my_url ='https://www.ebay.in/sch/i.html?_nkw='+search
		uClient=uReq(my_url)
		page_html=uClient.read()
		uClient.close()


		page_soup=soup(page_html,"html.parser")
		containers=page_soup.findAll("li",{"class":"sresult lvresult clearfix li shic"})
		#print(len(containers))
		dict ={}
		i=0
		for container in containers:
			i=i+1
			if i>5:
				break
			else:
							

				dict.update({'amazon'+str(i):{
					'title':container.findAll("h3",{"class":"lvtitle"})[0].a.text,
					'img':container.findAll("div",{"class":"lvpic pic img left"})[0].div.a.img["src"],
					'link_url' : container.findAll("div",{"class":"lvpic pic img left"})[0].div.a["href"],
					'price':container.findAll("li",{"class":"lvprice prc"})[0].text.strip(),
					
					

					}})

		
		return render_template('result.html',name=dict)

	return render_template('index.html')

if __name__ == "__main__":
	app.run()