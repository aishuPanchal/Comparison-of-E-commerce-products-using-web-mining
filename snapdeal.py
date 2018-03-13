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
		s = search.replace(' ','%20')
		my_url ='https://www.snapdeal.com/search?keyword='+search.replace(' ','%20')+'&sort=rlvncy'
		uClient=uReq(my_url)
		stime = time.time()
		page_html=uClient.read()
		etime = stime - time.time()
		print("time: " + str(etime))
		uClient.close()


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
				

				dict.update({'amazon'+str(i):{
					'title':container.div.a.p["title"],
					'img':imgsrc[i].a.picture.img["src"],
					'link_url' : container.div.a["href"],
					'price':container.findAll("span",{"class":"lfloat product-price"})[0].text.strip(),
					'rating': 'no rating'
					

					}})


		
		return render_template('result.html',name=dict)

	return render_template('index.html')

if __name__ == "__main__":
	app.run()