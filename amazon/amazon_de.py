from bs4 import BeautifulSoup as bs
from requests import Session
s = Session()
import sys
import csv
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
file = open("amazon_de.csv","w",newline="",encoding="utf-8")
row = csv.writer(file)

row.writerow(["product_name","product_price1","product_price2","image_url","product_href"])
def Crawl_List(url):
    r = s.get(url)
    soup = bs(r.content,"html.parser")
    for product in soup.find_all("div","a-section a-spacing-medium"):
        product_price1,product_price2="",""
        product_name = product.find("h2","a-size-mini a-spacing-none a-color-base s-line-clamp-4").text
        if product.find("span","a-price-whole"):
            product_price1 = product.find("span","a-price-whole").text
        if product.find("span","a-price a-text-price"):
            product_price2 = (product.find("span","a-price a-text-price").find("span","a-offscreen").text)              
        image_url = product.find("img","s-image").get("src")     
        product_href = product.find("a","a-link-normal s-no-outline").get("href")
        row.writerow([product_name,product_price1,product_price2,image_url,product_href])

    try:
        url_page = soup.find("div","a-section a-spacing-none s-result-item s-flex-full-width s-widget").find("li","a-last").find("a").get("href")
        print(soup.find("div","a-section a-spacing-none s-result-item s-flex-full-width s-widget").find("li","a-last").find("a").get("href"))
        Crawl_List("https://www.amazon.de"+url_page)
    except:
        sys.exit()    


urls = ["https://www.amazon.de/s?i=computers&bbn=427957031&rh=n%3A427957031%2Cp_89%3ALenovo%2Cp_n_feature_fourteen_browse-bin%3A8321930031%7C8321931031%2Cp_n_condition-type%3A776949031&dc&qid=1629094899&rnid=776942031&ref=sr_pg_1"]
for url in urls:
    Crawl_List(url)