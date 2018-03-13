from flask import Flask, render_template, request
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time

app = Flask(__name__)

@app.route('/send',methods=['GET','POST'])
def index():
	if request.method == 'POST':
		search = request.form['search']

		my_url =my_url ='https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords='+search
		uClient=uReq(my_url)
		stime = time.time()
		page_html=uClient.read()
		etime = stime - time.time()
		print("time: " + str(etime))
		uClient.close()


		page_soup=soup(page_html,"html.parser")
		containers=page_soup.findAll("div",{"class":"s-item-container"})
		
		dic ={}
		i=0
		for container in containers:
			
				contain = container.findAll("div",{"class":"a-fixed-left-grid-col a-col-right"})[0]
				imgsrc = container.findAll("div",{"class":"a-fixed-left-grid-col a-col-left"})[0]
				

				dic.update({'amazon'+str(i):{
					'title':contain.div.div.a["title"],
					'img':imgsrc.div.div.a.img["src"],
					'link_url' : contain.div.div.a["href"],
					'price':contain.findAll("span",{"class":"a-size-base a-color-price s-price a-text-bold"})[0].text.strip(),
					'rating': contain.findAll("span",{"class":"a-declarative"})[0].a.i.text
					
					}})


		
		return render_template('result.html',name=dic)

	return render_template('index.html')

if __name__ == "__main__":
	app.run()