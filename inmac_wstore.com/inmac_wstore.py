from bs4 import BeautifulSoup as bs
import time
from requests import Session
import csv
s  = Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
s.headers['Accept-Language'] = 'en-US,en;q=0.9'
s.headers['Accept-Encoding'] = 'gzip, deflate'
s.headers['Cookie'] = "mscssid_.www.inmac-wstore.comInmacwstore={6F188D6A-70BF-4617-9BC7-A0A04B2B4483}; _gcl_au=1.1.1201889772.1628416567; _gid=GA1.2.273040741.1628416567; _cs_c=1; axeptio_cookies={%22$$token%22:%22h1gr263utwgrlqk71r2ii%22%2C%22$$date%22:%222021-08-08T10:41:59.523Z%22%2C%22$$completed%22:true%2C%22ContentSquare%22:false%2C%22google_analytics%22:false%2C%22Bing%22:false%2C%22Criteo%22:false%2C%22effiliation%22:false%2C%22Google_Ads%22:false%2C%22IDE%22:false%2C%22Google_Conversion_Linker%22:false%2C%22Linkedin%22:false%2C%22vimeo%22:false%2C%22Idealo%22:false%2C%22Teads%22:false}; axeptio_all_vendors=%2CContentSquare%2Cgoogle_analytics%2CBing%2CCriteo%2Ceffiliation%2CGoogle_Ads%2CIDE%2CGoogle_Conversion_Linker%2CLinkedin%2Cvimeo%2CIdealo%2CTeads%2C; axeptio_authorized_vendors=%2C%2C; CookieLegal=1; ASP.NET_SessionId=t1caq5e2o2ofdsfexn4rljtg; __AntiXsrfToken=b9723460336749ac850c726339fbda7b; _cs_mk=0.12981803869576125_1628623706393; _gat_UA-1761154-1=1; _ga_SFH4MTD1G4=GS1.1.1628623706.6.1.1628624003.0; _ga=GA1.1.1248570493.1628415667; _cs_id=5d656431-5301-ac1b-ab64-37553e4c028b.1628416568.6.1628624004.1628623722.1.1662580568028.Lax.0; _cs_s=3.0.0.1628625804501; datadome=Ai-pfGc-No0eQOFoQSs4_57U6eULTkTYFb49kAvh4R0RXv.Z9mTzGlFYhWb8LwNHv9LUQHhQE6orTgA.vkRLHVuVy2MDLhlOGjSFzwqeEf"

file = open("inmac_wstore.csv","w",newline="",encoding="utf-8")
row = csv.writer(file)

row.writerow(["title","MRP_price","online_price","code","product_href"])
def detail_page(product_href):  
    r = s.get(product_href)
    soup = bs(r.content,"html.parser")
    title,MRP_price,online_price,code = '','','',''
    if soup.find("h1",attrs = {"itemprop":"name"}):
        title = soup.find("h1",attrs = {"itemprop":"name"}).text.strip()
    if soup.find("div","Tooltip_PriceTax_Link tip"):
        online_price = soup.find("div","Tooltip_PriceTax_Link tip").text.strip()
    if soup.find("div","priceTTC"):
        MRP_price  = soup.find("div","priceTTC").text.strip()
    if soup.find("div","brand-sku col-xs-24"):  
        code = (soup.find("div","brand-sku col-xs-24").text.strip().replace("Conçu par Lenovo/",""))

    return title,MRP_price,online_price,code

def Crawl_List():
    for URL in range(1,7):
        r = s.get(url="https://www.inmac-wstore.com/pc-portable/c507.htm?m=1265&p={}".format(URL))
        print(r.status_code)
        soup = bs(r.content,"html.parser")
        for href in soup.find_all("h2","ttShortTitle"):
            product_href = href.find("a").get("href")
            title,MRP_price,online_price,code = detail_page("https://www.inmac-wstore.com"+product_href)

            row.writerow([title,MRP_price,online_price,code,product_href])

Crawl_List() 