from db import Product, Root
from statistics import mean
import math
import get_html
import json
from requests_html import HTMLSession
import message

def check_products(products, s):
    result = list((object['id'] for object in products))

    prods_db = s.query(Product.market_id, Product.price).filter(Product.market_id.in_(result)).all()

    arrProds = {}
    for prods in prods_db:
        if prods[0] not in arrProds.keys():
            arrProds[prods[0]] = [prods[1]]
        else:
            arrProds[prods[0]].append(prods[1])

    prods_to_add = []
    for res in result:
        if res not in arrProds.keys():
            prods_to_add.append(res)
    to_add = {}
    root = []
    for prods in products:
            current_price = int(prods['salePriceU'] / 100)
            if prods['id'] in arrProds.keys():
                if len(arrProds[prods['id']]) and current_price not in arrProds[prods['id']]:

                    to_add[prods["id"]] = current_price
                    average = get_average(arrProds[prods['id']])
                    # average = mean(arrProds[prods['id']])
                    if current_price <= int(int(average['average']) * 0.5):

                        check_root = s.query(Root).filter(Root.root == prods['root']).count()
                        if check_root<1:
                            prods["average"] = average['average']
                            price_history = get_price_history(prods['id'])
                            id_c = str(prods['id'])[:-4]
                            img = f"https://images.wbstatic.net/c516x688/new/{id_c}0000/{prods['id']}-1.jpg"
                            if 'max' in price_history:
                                prods['price_max'] = price_history['max']
                            else:
                                 prods['price_max'] = 0
                            if 'min' in price_history:
                                 prods['price_min'] = price_history['min']
                            else:
                                prods['price_min'] = 0
                            prods['stock'] =  get_stock(prods['id'])
                            prods['image'] = img
                            prods['name'] = prods['brand'] + "/" + prods['name']
                            new_root = Root(root=prods['root'])


                            message.send_product_message(prods)
                            s.add(new_root)
                            s.commit()


            if prods['id'] in prods_to_add:
                    to_add[prods["id"]] = current_price


    arrToadd = []
    for key in to_add:
        pr = Product(market_id = key, price = to_add[key])
        arrToadd.append(pr)

    s.bulk_save_objects(arrToadd)
    s.commit()



def get_average(prices):
    result = {}
    if len(prices)==1:
        result = {
            'average': prices[0],
            'max':0,
            'min':0
        }
        return result

    elif len(prices)==2:
        result = {
            'average': int(mean(prices)),
            'max':max(prices),
            'min':min(prices)
        }
        return result

    elif len(prices) > 1 and len(prices) <= 5:
        prices.remove(max(prices))

        result = {
            'average': int(mean(prices)),
            'max': max(prices),
            'min': min(prices)
        }
        return result

    elif len(prices) > 5 and len(prices) <= 10:
        for i in range(1, 2):
            prices.remove(max(prices))
        result = {
            'average': int(mean(prices)),
            'max': max(prices),
            'min': min(prices)
        }
        return result

    elif len(prices) > 10 and len(prices) <= 15:
        for i in range(1, 3):
            prices.remove(max(prices))
        result = {
            'average': int(mean(prices)),
            'max': max(prices),
            'min': min(prices)
        }
        return result

    elif len(prices) > 16:
        prices = prices[-15:]
        for i in range(1, 3):
            prices.remove(max(prices))
        result = {
            'average': int(mean(prices)),
            'max': max(prices),
            'min': min(prices)
        }
        return result
    return {
            'average': 0,
            'max': 0,
            'min': 0
        }

def get_price_history(id):
    url = f'https://wbx-content-v2.wbstatic.net/price-history/{str(id)}.json'
    try:
        price_history = get_html.get_html(url)
    except:
        price_history = ''
    history = {}
    if price_history:
        parse = json.loads(price_history)
        lenth_list = len(parse)
        price_list = []
        for n in range(lenth_list):
            price_list.append(math.ceil(parse[n]['price']['RUB'] / 100))
        maximum = max(price_list)
        minimum = min(price_list)
        history['max'] = maximum
        history['min'] = minimum

    return history

def get_stock(id):
    url = f'https://catalog.wb.ru/catalog/nm-2-card/catalog?stores=117673,122258,122259,125238,125239,125240,6159,507,3158,117501,120602,120762,6158,121709,124731,159402,2737,130744,117986,1733,686,132043&appType=1&locale=ru&lang=ru&curr=rub&dest=-1029256,-102269,-1278703,-1255563&nm={id}'
    url =f"https://card.wb.ru/cards/detail?spp=0&regions=80,68,64,83,4,38,33,70,82,69,86,30,40,48,1,22,66,31&pricemarginCoeff=1.0&reg=0&appType=1&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=2,7,3,6,19,21,8&dest=-1059500,-108082,-269701,12358063&nm={id}"

    html = get_html.get_html(url)
    s = json.loads(html)
    sizes = s['data']['products'][0]['sizes']
    stock = 0
    try:
        for size in sizes:
            if len(size['stocks']) > 0:
                for wh in size['stocks']:
                    stock += int(wh['qty'])
    except:
        stock = 0
    return stock


def get_image(id):
    session = HTMLSession()
    url = f'https://www.wildberries.ru/catalog/{id}/detail.aspx?targetUrl=GP'
    r = session.get(url)
    data = {}
    try:
        r.html.render(sleep=3)

        try:
            data['image'] = r.html.find('.photo-zoom__preview', first=True).attrs['src']
        except:
            data['image']
        try:
            data['name'] = r.html.find('h1', first=True).text.strip()
        except:
            data['name'] = ''
    except:
        data['image'] = 'https://netsh.pp.ua/wp-content/uploads/2017/08/Placeholder-1.png'
        data['name'] = ''
    r.close()
    session.close()
    del r
    del session
    return data
