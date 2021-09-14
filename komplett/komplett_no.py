from bs4 import BeautifulSoup as bs
from requests import Session
from time import strftime
from lxml import html
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
import mysql.connector
con = mysql.connector.connect(host='localhost',user='root',password='root',database='crawling',charset='utf8',use_unicode=True)
cur = con.cursor()


def crawling_detailpage(url):
    r = s.get(url)
    tree = html.fromstring(r.text)
    retailer = 'komplett'
    country = 'norway'
    extraction_date = strftime("%A, %d %b %Y ,%r")
    name = ''.join(tree.xpath('//h1[@class="product-main-info-webtext1"]//span//text()')).strip()
    reg_price = ''.join(tree.xpath('//div[@class="product-price "]//span[@class="product-price-now"]//text()')).strip()
    discounted_price = ''
    model_no = ''.join(tree.xpath('//div[@class="product-main-info-partnumber-store hide-xs"]//span[@itemprop="sku"]//text()')).strip()
    part_no = ''.join(tree.xpath('//div[@class="product-main-info-partnumber-store hide-xs"]//span[@itemprop="mpn"]//text()')).strip()
    stock = ''
    if tree.xpath('//div[@class="product-main-info-buy-button"]//span[@class="text"][contains(string(),"Legg i handlevogn")]'):
        stock = 'In stock'
    else:
        stock = 'Out of stock'    

    try:
        table = "create table komplett_no(retailer varchar(100),country varchar(100),extraction_date varchar(100),name varchar(500) null,reg_price varchar(400) null COLLATE utf8_unicode_ci,discounted_price varchar(400) null COLLATE utf8_unicode_ci,part_no varchar(200) null COLLATE utf8_unicode_ci,model_no varchar(200) null COLLATE utf8_unicode_ci,stock varchar(500) null)"
        cur.execute(table)
        con.commit()
        query = "insert into komplett_no(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit() 
    except:
        query = "insert into komplett_no(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit()

    print("\n===========\n",part_no,"\n",model_no,"\n",name,"\n",reg_price,"\n",discounted_price,"\n",stock,"\n",extraction_date,"\n=============\n")



def crawling_listpage(url):
    r = s.get(url)
    soup = bs(r.content,"html.parser")
    for products in soup.find_all("div","product-list-item"):
        product_href = products.find("a","product-link").get("href")
        print(products.find("a","product-link").get("href"))
        crawling_detailpage("https://www.komplett.no"+product_href)


urls = ['https://www.komplett.no/category/11156/pc-nettbrett/pc-baerbar/laptop/alle-pc-er?nlevel=10723%C2%A710011%C2%A711156&manufacturer=Lenovo&hits=72']
for url in urls:
    crawling_listpage(url)