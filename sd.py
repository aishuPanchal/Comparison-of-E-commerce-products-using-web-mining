import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url ='https://www.snapdeal.com/search?keyword=moto&sort=rlvncy'

uClient=uReq(my_url)
page_html=uClient.read()
uClient.close()

page_soup=soup(page_html,"html.parser")

containers=page_soup.findAll("div",{"class":"product-tuple-description "})
imgsrc=page_soup.findAll("div",{"class":"product-tuple-image "})
print(len(containers))
i=0
for container in containers:

	link_url=container.div.a["href"]
	img = imgsrc[i].a.picture.img["src"]
	i=i+1
	title = container.div.a.p["title"]
	price = container.findAll("span",{"class":"lfloat product-price"})[0].text.strip()

	print("title : "+title)
	print("price : "+price)
	print("Link : "+link_url)
	print("img : "+img)