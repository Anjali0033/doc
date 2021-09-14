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
    retailer = 'cyberport'
    country = 'germany'
    extraction_date = strftime("%A, %d %b %Y ,%r")
    name = ''.join(tree.xpath('//div[@class="title"]//text()')).replace('%Sale','').strip()
    reg_price = ''.join(tree.xpath('//span[@class="oldPrice"]//text()')).strip()
    discounted_price = ''.join(tree.xpath('//div[@class="price delivery-price orange"]//text()')).strip()
    part_no = ''.join(tree.xpath('//div[@class="productNumbers"]//span[@class="manufacturerNumber copySmall"]//text()')).strip().replace("Herstellernummer: ","")
    model_no = ''.join(tree.xpath('//div[@class="productID"]//text()')).strip().replace("Artikelnummer: ","")
    stock = ''.join(tree.xpath('//span[@class="tooltipAppend available"]//text()')).strip()

    try:
        table = "create table notebooksbilliger_de(retailer varchar(100),country varchar(100),extraction_date varchar(100),name varchar(500) null,reg_price varchar(400) null COLLATE utf8_unicode_ci,discounted_price varchar(400) null COLLATE utf8_unicode_ci,part_no varchar(200) null COLLATE utf8_unicode_ci,model_no varchar(200) null COLLATE utf8_unicode_ci,stock varchar(500) null)"
        cur.execute(table)
        con.commit()
        query = "insert into notebooksbilliger_de(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit() 
    except:
        query = "insert into notebooksbilliger_de(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit()
        # pass        

    print("\n===========\n",part_no,"\n",model_no,"\n",name,"\n",reg_price,"\n",discounted_price,"\n",stock,"\n",extraction_date,"\n=============\n")


def crawling_listpage(url):
    r = s.get(url)
    soup = bs(r.content,"html.parser")
    for products in soup.find_all("article","productArticle"):
        product_href = products.find("a","head heading-level3").get("href")
        crawling_detailpage("https://www.cyberport.de"+product_href)

        
    if soup.find("a","sortList nextLink"):
        print(soup.find("a","sortList nextLink").get("href"))   
        url_page = soup.find("a","sortList nextLink").get("href")
        crawling_listpage("https://www.cyberport.de"+url_page)

urls = ['https://www.cyberport.de/markenshops/lenovo/notebooks.html?productsPerPage=24&sort=popularity&manufacturerName=Lenovo&page=1']
for url in urls:
    crawling_listpage(url)