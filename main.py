import requests

from  category import Category
from multiprocessing import Pool
from config import potok
# from products import get_products_from_category, clear_root
import time
from get_html import get_html
import traceback
import json
from sqlalchemy import create_engine, select

from sqlalchemy.orm import sessionmaker
from config import host, USER, passwd, database, port
from check_product import check_products

conn = "mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(USER, passwd, host, port, database)
engine = create_engine(conn)
session = sessionmaker(bind=engine)


def get_products_from_category(params):
    # url = f'https://catalog.wb.ru/catalog/{params["shard"]}/v4/filters?appType=1&curr=rub&lang=ru&locale=ru&pricemarginCoeff=1.0&reg=0&spp=0&stores=117673,122258,122259,125238,125239,125240,6159,507,3158,117501,120602,120762,6158,121709,124731,159402,2737,130744,117986,1733,686,132043&{params["query"]}'
    url = f"https://catalog.wb.ru/catalog/{params['shard']}/catalog?curr=rub&lang=ru&locale=ru&sort=priceup&{params['query'].replace('subject', 'xsubject')}&page={1}"
    js = requests.get(url)
    print(url)
    category_products=[]
    if js:
        try:
            js = json.loads(js.text)
            for i in range(1, int(100)):
                print(i, params['shard'])
                # url_category =f"https://catalog.wb.ru/catalog/{params['shard']}/catalog?appType=1&couponsGeo=2,7,3,6,19,21,8&curr=rub&emp=0&lang=ru&locale=ru&page={i}&pricemarginCoeff=1.0&sort=sale&spp=0&{params['query']}"
                # url_category = f'https://catalog.wb.ru/catalog/{params["shard"]}/catalog?appType=1&curr=rub&kind=2&lang=ru&locale=ru&pricemarginCoeff=1.0&reg=0&sort=sale&page={i}&{params["query"]}'
                r = requests.get(f"https://catalog.wb.ru/catalog/{params['shard']}/catalog?curr=rub&lang=ru&locale=ru&sort=priceup&{params['query'].replace('subject', 'xsubject')}&page={i}")

                try:
                    json_prods = json.loads(r.text)
                    if json_prods['data']['products']:
                        for product in json_prods['data']['products']:
                            category_products.append(product)
                    else:
                        break
                except:
                    break



        except Exception:
                traceback.print_exc()
        s = session()
        if category_products:
            check_products(category_products, s)








def main():
    start_time = time.time()
    category = Category()
    categoryLinks = category.get_category_links()
    print(len(categoryLinks))
    with Pool(potok) as p:
        p.map(get_products_from_category, categoryLinks)
    # while True:
        # time.sleep(1)
        # proxies.main()
        # clear_root()
        # category_links = categories.get_category_links()
        # print (len(category_links))
        # with Pool(potok) as p:
        #     p.map(get_products_from_category, category_links)
        # # for link in category_links:
        # #     get_products_from_category(link)
        # print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == '__main__':
    main()