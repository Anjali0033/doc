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
    retailer = 'redcorp'
    country = 'Belgium'
    extraction_date = strftime("%r, %d %b %Y ,%A")    
    name = ''.join(tree.xpath('//div[@class="heading-bar__heading"]//h1//text()')).replace("LENOVO","").strip()
    reg_price = ''.join(tree.xpath('//div[@class="price-block text-center"]//div[@class="current-row__price"]//text()')).replace('Excl. VAT','').strip()
    discounted_price = ''.join(tree.xpath('//div[@class="contact-block__text"]//strong//text()')).replace('Starts from','').replace('Details','').strip()
    part_no = ''.join(tree.xpath('//div[@class="specification__brand flexed is-narrow flexed--center hidden-small"]//div[@class="brand__cle"]//span[2]//text()')).replace("Article# ","")
    model_no = ''.join(tree.xpath('//div[@class="specification__brand flexed is-narrow flexed--center hidden-small"]//div[@class="brand__cle"]//span[1]//text()')).replace("Redcorp# ","")
    stock = ''
    if tree.xpath('//div[@class="col-md-9 col-xs-9 green"]//span[@class="Gray"][contains(string(),"Out of Stock.")]'):
        stock = 'stock not available'
    else:
        stock = 'stock available'    

    try:
        table = "create table redcorp(retailer varchar(100),country varchar(100),extraction_date varchar(100),name varchar(500) null,reg_price varchar(400) null COLLATE utf8_unicode_ci,discounted_price varchar(400) null COLLATE utf8_unicode_ci,part_no varchar(200) null COLLATE utf8_unicode_ci,model_no varchar(200) null COLLATE utf8_unicode_ci,stock varchar(500) null)"
        cur.execute(table)
        con.commit()
        query = "insert into redcorp(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit() 
    except:
        query = "insert into redcorp(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit()

    print("\n===========\n",part_no,"\n",model_no,"\n",name,"\n",reg_price,"\n",discounted_price,"\n",extraction_date,"\n",stock,"\n=============\n")



def crawling_listpage(url):
    r = s.get(url)
    soup = bs(r.content,"html.parser")
    for products in soup.find_all("div","card list-view"):
        product_href = products.find("div","list-view__prod-name").find("a").get("href")
        crawling_detailpage("https://www.redcorp.com"+product_href)

    for i in (soup.find_all("li")):
        if(i.find("a",attrs={"aria-label":"Next"})):
            print(i.find("a",attrs={"aria-label":"Next"}).get("href"))   
            url_page = i.find("a",attrs={"aria-label":"Next"}).get("href")
            crawling_listpage("https://www.redcorp.com"+url_page)


urls = ['https://www.redcorp.com/en/QuickFinder/2/computing-notebooks-laptops-and-ultrabooks?f_Manufacturer=LENOVO&page=1']
for url in urls:
    crawling_listpage(url)