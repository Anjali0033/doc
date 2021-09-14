from bs4 import BeautifulSoup as bs
from time import strftime
from requests import Session
s = Session()
import mysql.connector
con = mysql.connector.connect(host='localhost',user='root',password='root',database='crawling',charset='utf8',use_unicode=True)
cur = con.cursor()

def crawling_listpage(url):
    r = s.get(url)
    soup = bs(r.content,"html.parser")
    for products in soup.find_all("div","product-list-item row row-eq-height se-prd pli0"):
        retailer = 'beachtle'
        country = 'german'
        extraction_date = strftime("%A, %d %b %Y ,%r")        
        name = products.find("div","h-h3").text
        reg_price = products.find("div","footnote").text.split("€")[0].replace("Bruttopreis:","").strip()
        discounted_price = products.find("p","bechtle-price bechtle-price-list").text.strip()
        part_no = products.find("div","product-description").find("p","data-text").text.replace("Hersteller-Nr.:","").strip()
        model_no = products.find("div","product-description").find_all("p","data-text")[1].text.replace("Bechtle-Nr.:","").strip()
        stock = ''
        if products.find("div","delivery-info outofstock"):
            stock = "out of stock"
        else:
            stock = "In stock"

        try:
            table = "create table beachtle_de(retailer varchar(100),country varchar(100),extraction_date varchar(100),name varchar(500) null,reg_price varchar(400) null COLLATE utf8_unicode_ci,discounted_price varchar(400) null COLLATE utf8_unicode_ci,part_no varchar(200) null COLLATE utf8_unicode_ci,model_no varchar(200) null COLLATE utf8_unicode_ci,stock varchar(500) null)"
            cur.execute(table)
            con.commit()
            query = "insert into beachtle_de(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
            cur.execute(query,VALUES)
            con.commit() 
        except:
            query = "insert into beachtle_de(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
            cur.execute(query,VALUES)
            con.commit()

        print("\n===========\n",part_no,"\n",model_no,"\n",name,"\n",reg_price,"\n",discounted_price,"\n",stock,"\n",extraction_date,"\n=============\n")


urls = ["https://www.bechtle.com/shop/hardware/mobile-computing/notebooks--10007004--c/lenovo"]
for url in urls:
    crawling_listpage(url)