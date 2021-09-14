from bs4 import BeautifulSoup as bs
from time import strftime
from requests import Session
from lxml import html
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
import mysql.connector
con = mysql.connector.connect(host='localhost',user='root',password='root',database='crawling',charset='utf8',use_unicode=True)
cur = con.cursor()
# 
def crawling_detailpage(url):
    r = s.get(url)
    tree = html.fromstring(r.text)
    retailer = 'computersalg'
    country = 'norway'
    extraction_date = strftime("%A, %d %b %Y ,%r")
    name = ''.join(tree.xpath('//header[@class="product-header grid_20"]//h1[@itemprop="name"]//text()')).strip()
    reg_price = ''.join(tree.xpath('//div[@class="productPrice"]//div[@class="grey"][1]//text()')).strip().replace("eksklusiv MVA ","")

    discounted_price = ''.join(tree.xpath('//div[@class="productPrice"]//div[@class="grey"][2]//text()')).replace("Totalt inkl. frakt ","").strip()
    part_no = ''.join(tree.xpath('//h2[@class="productIdentifierHeadline"]//span[4]//text()')).strip()
    model_no = ''.join(tree.xpath('//h2[@class="productIdentifierHeadline"]//span[3]//text()')).strip()
    stock=''
    if tree.xpath('//div[@class="campaign"]//h4[contains(string(),"Utsolgt")]'):
        stock = "stock not available"
    else:
        stock = "stock available"

    try:
        table = "create table computersalg_no(retailer varchar(100),country varchar(100),extraction_date varchar(100),name varchar(500) null,reg_price varchar(400) null COLLATE utf8_unicode_ci,discounted_price varchar(400) null COLLATE utf8_unicode_ci,part_no varchar(200) null COLLATE utf8_unicode_ci,model_no varchar(200) null COLLATE utf8_unicode_ci,stock varchar(500) null)"
        cur.execute(table)
        con.commit()
        query = "insert into computersalg_no(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit() 
    except:
        query = "insert into computersalg_no(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit()

    print("\n===========\n",part_no,"\n",model_no,"\n",name,"\n",reg_price,"\n",discounted_price,"\n",stock,"\n",extraction_date,"\n=============\n")


def crawling_listpage(url):
    r = s.get(url)
    soup = bs(r.content,"html.parser")
    for products in soup.find_all("li","tool-list-product productlist-item"):
        product_href = products.find("a","itemclikevent productNameLink").get("href")
        crawling_detailpage("https://www.computersalg.no"+product_href)

    print(url)

for i in range(1,28):
    url = 'https://www.computersalg.no/l/1393/b%C3%A6rbar?p={}&f=958caa69-e7b1-4423-b228-940fae96a340&sq='.format(i)
    crawling_listpage(url)