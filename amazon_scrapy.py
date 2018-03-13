import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url ='https://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=oneplus5'

uClient=uReq(my_url)
page_html=uClient.read()
uClient.close()

page_soup=soup(page_html,"html.parser")

containers=page_soup.findAll("div",{"class":"s-item-container"})

for container in containers:
	product_name = container.findAll("h2").text
	
	price = container.findAll("span",{"class":"a-size-base a-color-price s-price a-text-bold"})[0].text.strip()
	rating =  container.findAll("span",{"name":"B0756ZFXVB"})[0].text.strip()
	
	
	