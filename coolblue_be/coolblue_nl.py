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
    print(r.status_code)
    tree = html.fromstring(r.text)
    retailer = 'coolblue'
    country = 'Netherlands'
    extraction_date = strftime("%A, %d %b %Y ,%r")
    name = ''.join(tree.xpath('//div[@class="section--2@md"]//h1[@class="js-product-name "]//text()')).strip()
    reg_price = ''.join(tree.xpath('//div[@class="js-threshold-toggle-sticky-bar"]//span[@class="sales-price__former"]//span[@class="sales-price__former-price"]//text()')).strip()
    discounted_price = ''.join(tree.xpath('//div[@class="js-threshold-toggle-sticky-bar"]//span[@class="sales-price sales-price--same-font-size js-sales-price"]//strong[@class="sales-price__current"]//text()')).strip()
    part_no = ''.join(tree.xpath('//div[@class="product-specs"]//dl//dt[contains(string(),"Manufacturer code")]//ancestor::dl//dd//text()')).strip()
    model_no = ''.join(tree.xpath('//div[@class="product-specs"]//dl//dt[contains(string(),"Product number")]//ancestor::dl//dd//text()')).strip()
    stock=''
    if tree.xpath('//div[@class="section--5@md"]//span[@class="hide@md-down js-order-button"][contains(string(),"In my shopping cart")]'):
        stock = "stock available"
    elif tree.xpath('//div[@class="section--5@md"]//div[@class="icon-with-text__text"][contains(string(),"Keep me updated")]'):
        stock = "stock not available"

    try:
        table = "create table coolblue_nl(retailer varchar(100),country varchar(100),extraction_date varchar(100),name varchar(500) null,reg_price varchar(400) null COLLATE utf8_unicode_ci,discounted_price varchar(400) null COLLATE utf8_unicode_ci,part_no varchar(200) null COLLATE utf8_unicode_ci,model_no varchar(200) null COLLATE utf8_unicode_ci,stock varchar(500) null)"
        cur.execute(table)
        con.commit()
        query = "insert into coolblue_nl(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit() 
    except:
        query = "insert into coolblue_nl(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit()

    print("\n===========\n",part_no,"\n",model_no,"\n",name,"\n",reg_price,"\n",discounted_price,"\n",stock,"\n",extraction_date,"\n=============\n")


def crawling_listpage(url):
    r = s.get(url)
    soup = bs(r.content,"html.parser")
    tree = html.fromstring(r.text)
    for products in soup.find_all("div","product-card"):
        product_href = products.find("a","link d--block").get("href")
        crawling_detailpage("https://www.coolblue.nl"+product_href)

    if tree.xpath('//div[@class="flex justify-content--center"]//li[@class="pagination__item pagination__item--arrow"]//a[@class="pagination__link  "]'):
        print(tree.xpath('//div[@class="flex justify-content--center"]//li[@class="pagination__item pagination__item--arrow"]//a[@class="pagination__link  "]//@href'))
        url_page = ''.join(tree.xpath('//div[@class="flex justify-content--center"]//li[@class="pagination__item pagination__item--arrow"]//a[@class="pagination__link  "]//@href'))
        crawling_listpage("https://www.coolblue.nl/en/laptops/lenovo"+url_page)

urls = ['https://www.coolblue.nl/en/laptops/lenovo']
for url in urls:
    crawling_listpage(url)