from bs4 import BeautifulSoup as bs
from time import strftime
from requests import Session
from lxml import html
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
import mysql.connector
con = mysql.connector.connect(host='localhost',user='root',password='root',database='crawling',charset='utf8',use_unicode=True)
cur = con.cursor()

def crawling_detailpage(url):
    r = s.get(url)
    tree = html.fromstring(r.text)
    retailer = 'coolblue'
    country = 'Belgium'
    extraction_date = strftime("%A, %d %b %Y ,%r")
    name = ''.join(tree.xpath('//div[@class="section--2@md"]//h1[@class="js-product-name "]//text()')).strip()
    reg_price = ''.join(tree.xpath('//div[@class="hide@md-down"]//form[@class="js-product-order-form"]//span[@class="sales-price__former-price"]//text()')).strip()
    discounted_price = ''.join(tree.xpath('//div[@class="hide@md-down"]//form[@class="js-product-order-form"]//strong[@class="sales-price__current"]//text()')).strip()
    part_no = ''.join(tree.xpath('//div[@class="product-specs"]//dl//dt[@class="product-specs__item-title js-spec-title"][contains(string(),"Fabrikantcode")]//ancestor::dl//dd//text()')).strip()
    model_no = ''.join(tree.xpath('//div[@class="product-specs"]//dl//dt[@class="product-specs__item-title js-spec-title"][contains(string(),"Artikelnummer")]//ancestor::dl//dd//text()')).strip()
    stock=''
    if tree.xpath('//div[@class="section--5@md"]//span[@class="hide@md-down js-order-button"][contains(string(),"In mijn winkelwagen")]'):
        stock = "stock available"
    elif tree.xpath('//div[@class="icon-with-text icon-with-text--centered-vertical"]//div[@class="icon-with-text__text"][contains(string(),"Houd mij op de hoogte")]'):
        stock = "stock not available"

    try:
        table = "create table coolblue_be(retailer varchar(100),country varchar(100),extraction_date varchar(100),name varchar(500) null,reg_price varchar(400) null COLLATE utf8_unicode_ci,discounted_price varchar(400) null COLLATE utf8_unicode_ci,part_no varchar(200) null COLLATE utf8_unicode_ci,model_no varchar(200) null COLLATE utf8_unicode_ci,stock varchar(500) null)"
        cur.execute(table)
        con.commit()
        query = "insert into coolblue_be(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit() 
    except:
        query = "insert into coolblue_be(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit()

    print("\n===========\n",part_no,"\n",model_no,"\n",name,"\n",reg_price,"\n",discounted_price,"\n",stock,"\n",extraction_date,"\n=============\n")


def crawling_listpage(url):
    r = s.get(url)
    soup = bs(r.content,"html.parser")
    for products in soup.find_all("div","product-card"):
        product_href = products.find("div","h3 mt--4@md").find("a","link").get("href")
        crawling_detailpage("https://www.coolblue.be"+product_href)

    for i in  (soup.find("ul","pagination").find_all("li","pagination__item")):
        if soup.find("ul","pagination").find_all("li","pagination__item"):
            if i.find("a",attrs={"aria-label":"Ga naar de volgende pagina"}):
                print(i.find("a",attrs={"aria-label":"Ga naar de volgende pagina"}).get("href"))
                url_page = i.find("a",attrs={"aria-label":"Ga naar de volgende pagina"}).get("href")
                crawling_listpage("https://www.coolblue.be/nl/laptops/filter/merk:lenovo"+url_page)
    

urls = ['https://www.coolblue.be/nl/laptops/filter/merk:lenovo?pagina=1']
for url in urls:
    crawling_listpage(url)