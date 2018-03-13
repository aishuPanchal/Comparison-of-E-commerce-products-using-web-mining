import flipkart
import amazon
import ebay

from amazon import *
from ebay import *
from flipkart import *

#print(name)
#amazon.myfunc()

text = input("prompt")
t1=text
print(text)


print("printing db from another file*****************************************************")

cursor = collection.find({"name": {"$regex": t1, "$options": "i"}})
print(cursor.count())
if(cursor.count()>0):
	for document in cursor:
		print("###################################### printing from database #############################################")
		pprint(document)
		print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
		print(document["name"])
		print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

else:
	flipkart.myfunc(text)
	amazon.myfunc(text)
	ebay.myfunc(text)
	
	print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! we crawled first !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	cursor = collection.find({"name": {"$regex": t1, "$options": "i"}})
	print(cursor.count())
