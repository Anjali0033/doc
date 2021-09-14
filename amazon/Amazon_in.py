from bs4 import BeautifulSoup as bs 
from requests import Session
import csv
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"

file = open("amazon_lenovo.csv","w",newline="",encoding="utf-8")
row = csv.writer(file)

row.writerow(["Title","Online_price","MRP_price","image_url","Product_href"])
def crawl_list(url):  
    r = s.get(url)
    soup =  bs(r.content,'html.parser')
    products = soup.find_all("div","sg-col-inner")

    for product in products:
        title,online_price,MRP_price,image_url,product_href='','','','',''
        if product.find("h2","a-size-mini a-spacing-none a-color-base s-line-clamp-4"):
            title = product.find("h2","a-size-mini a-spacing-none a-color-base s-line-clamp-4").text.strip()
        if product.find("span","a-price-whole"):
            online_price = product.find("span","a-price-whole").text.strip()
        if product.find("span","a-price a-text-price"):
            MRP_price = product.find("span","a-price a-text-price").text.strip()
        if product.find("img","s-image"):
            image_url = product.find("img","s-image").get("src")   
        if product.find("a","a-size-base a-link-normal a-text-normal"):
            product_href = product.find("a","a-size-base a-link-normal a-text-normal").get("href")
        row.writerow([title,online_price,MRP_price,image_url,product_href])
    
    try:       
        url_page = soup.find("div","a-section a-spacing-none s-result-item s-flex-full-width s-widget").find("a","s-pagination-item s-pagination-next s-pagination-button s-pagination-separator").get("href")
        crawl_list("https://www.amazon.in"+url_page)
    except:
        pass   

URL=['https://www.amazon.in/s?i=computers&rh=n%3A4364644031&fs=true&page=2&qid=1628616281&ref=sr_pg_1']
for i in URL:
    crawl_list(i)