from bs4 import BeautifulSoup as bs
from time import strftime
import csv
from requests import Session
s = Session()
file = open("beachtle_de.csv","w",newline="",encoding="utf-8")
row = csv.writer(file)
row.writerow(["retailer","country","extraction_date","name","reg_price","discounted_price","part_no","model_no","stock"])


for i in range(0,311,20):
        r = s.get(url = "https://www.bechtle.com/shop/hardware/mobile-computing/notebooks--10007004--c/lenovo?size={}".format(i))
        soup = bs(r.content,"html.parser")
        print(r)
        for products in soup.find_all("div","product-list-item row row-eq-height se-prd pli0"):
            retailer = 'beachtle'
            country = 'german'
            extraction_date = strftime("%A, %d %b %Y ,%r")  
            name = (products.find("div","h-h3").text)
            if products.find("div","footnote"): reg_price = products.find("div","footnote").text.split("€")[0].replace("Bruttopreis:","").strip()
            else: reg_price = ""
            if products.find("p","bechtle-price bechtle-price-list"):discounted_price = products.find("p","bechtle-price bechtle-price-list").text.strip()
            else: discounted_price = ''
            part_no = products.find("div","product-description").find("p","data-text").text.replace("Hersteller-Nr.:","").strip()
            model_no = products.find("div","product-description").find_all("p","data-text")[1].text.replace("Bechtle-Nr.:","").strip()
            stock = ''
            if products.find("div","delivery-info outofstock"):
                stock = "out of stock"
            else:
                stock = "In stock"
            print("\n===========\n",part_no,"\n",model_no,"\n",name,"\n",reg_price,"\n",discounted_price,"\n",stock,"\n",extraction_date,"\n=============\n")

            row.writerow([retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock])