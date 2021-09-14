from bs4 import BeautifulSoup as bs
from lxml import html
from time import strftime
from requests import Session
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
import mysql.connector
con = mysql.connector.connect(host='localhost',user='root',password='root',database='crawling',charset='utf8',use_unicode=True)
cur = con.cursor()

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

    # try:
        # table = "create table fnac_fr(retailer varchar(100),country varchar(100),extraction_date varchar(100),name varchar(500) null,reg_price varchar(400) null COLLATE utf8_unicode_ci,discounted_price varchar(400) null COLLATE utf8_unicode_ci,part_no varchar(200) null COLLATE utf8_unicode_ci,model_no varchar(200) null COLLATE utf8_unicode_ci,stock varchar(500) null)"
        # cur.execute(table)
        # con.commit()
        # query = "insert into fnac_fr(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        # VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        # cur.execute(query,VALUES)
        # con.commit() 
    # except:
        # query = "insert into fnac_fr(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        # VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        # cur.execute(query,VALUES)
        # con.commit()
# 
    print("\n===========\n","\n",name,"\n",reg_price,"\n",discounted_price,"\n",stock,"\n",extraction_date,"\n=============\n")




def crawling_listpage(url):
    r = s.get(url)
    tree = html.fromstring(r.text)
    soup = bs(r.content,"html.parser")

    for products in soup.find_all("div","clearfix Article-item js-Search-hashLinkId"):
        product_href = products.find("a","Article-title js-minifa-title js-Search-hashLink").get("href")
        print(products.find("a","Article-title js-minifa-title js-Search-hashLink").get("href"))
        crawling_detailpage(product_href)


urls = ['https://www.fnac.com/Tous-les-ordinateurs-portables/Ordinateurs-portables/nsh154425/w-4?SFilt=62158!23&sl']
for url in urls:
    crawling_listpage(url)