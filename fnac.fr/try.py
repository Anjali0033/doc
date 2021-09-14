from bs4 import BeautifulSoup as bs
from time import strftime
import csv
from requests import Session, models
s = Session()
from lxml import html
x = []
file = open("fnac_fr.csv","w",newline="",encoding="utf-8")
row = csv.writer(file)
row.writerow(["retailer","country","extraction_date","name","reg_price","discounted_price","part_no","model_no","stock"])

def crawling_detailpage(url):
    r = s.get(url)
    tree = html.fromstring(r.text)
    retailer = 'fnac'
    country = 'france'
    extraction_date = strftime("%A, %d %b %Y ,%r")
    name = ''.join(tree.xpath('//h1[@class="f-productHeader-Title"]//text()')).strip()
    reg_price = ''.join(tree.xpath('//div[@class="f-priceBox"]//span[@class="f-priceBox-price f-priceBox-price--old"]//text()')).strip().replace("€",".")
    discounted_price = ''.join(tree.xpath('//div[@class="f-priceBox"]//span[@class="f-priceBox-price f-priceBox-price--reco checked"]//text()')).strip().replace("€",".")
    stock = ''
    if tree.xpath('//div[@class="bigPricerFA clearfix"]//span[@class="ff-button-label"][contains(string(),"Voir stock en magasin")]'):
        stock = 'out of stock'
    else:
        stock = 'In stock'    
    row.writerow([retailer,country,extraction_date,name,reg_price,discounted_price,stock])

    print("\n===========\n",name,"\n",reg_price,"\n",discounted_price,"\n",stock,"\n",extraction_date,"\n=============\n")


for i in range(0,58,18):
        r = s.get(url = "https://www.fnac.com/Tous-les-ordinateurs-portables/Ordinateurs-portables/nsh154425/w-4?PageIndex={}&SFilt=62158!23".format(i))
        soup = bs(r.content,"html.parser")
        print(r)
        
        for products in soup.find_all("div","clearfix Article-item js-Search-hashLinkId"):
            product_href = products.find("a","Article-title js-minifa-title js-Search-hashLink").get("href")
            print(products.find("a","Article-title js-minifa-title js-Search-hashLink").get("href"))
            x.append(products.find("a","Article-title js-minifa-title js-Search-hashLink").get("href"))
            


