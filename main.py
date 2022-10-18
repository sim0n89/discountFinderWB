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
    url = f'https://catalog.wb.ru/catalog/{params["shard"]}/v4/filters?appType=1&curr=rub&lang=ru&locale=ru&pricemarginCoeff=1.0&reg=0&spp=0&stores=117673,122258,122259,125238,125239,125240,6159,507,3158,117501,120602,120762,6158,121709,124731,159402,2737,130744,117986,1733,686,132043&{params["query"]}'
    r = get_html(url)
    if r:
        try:
            js = json.loads(r)
            total = js['data']['total']
            pages = int(total / 100)
            category_products = []
            if pages > 50:
                pages = 50
            elif pages < 1:
                pages = 1
            for i in range(1, int(pages)):
                url_category = f'https://catalog.wb.ru/catalog/{params["shard"]}/catalog?appType=1&curr=rub&kind=2&lang=ru&locale=ru&pricemarginCoeff=1.0&reg=0&sort=sale&page={i}&{params["query"]}'
                pr_list = get_html(url_category)
                json_prods = json.loads(pr_list)
                for product in json_prods['data']['products']:
                    category_products.append(product)
        except Exception:
                traceback.print_exc()
        s = session()
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