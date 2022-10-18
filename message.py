from config import TOKEN, channel_id
import telebot
import traceback
import gc

bot = telebot.TeleBot(TOKEN)


def send_message(message):
    try:
        bot.send_message(channel_id, message)
    except Exception:
        traceback.print_exc()


def send_product_message(product):
    product_message = make_product_message(product)
    bot.send_photo(channel_id, product['image'], parse_mode="html", caption=product_message)


def make_product_message(product):
    print(product)
    price = int(product['salePriceU'] / 100)
    del_price = int(product['priceU'] / 100)
    smile = '🤑'
    diap_text = ''
    # percent = int(100 - (price / product["average"]) * 100)
    if "price_min" in product and "price_max" in product:
        if product["price_min"] != product["price_max"]:
            diap_text = f'↔️Диапозон: {product["price_min"]}₽ - {product["price_max"]}₽'
            if price > product["price_max"]:
                smile = '📈'
            elif price < product['price_min']:
                smile = '📉'
            elif price < product["price_max"] and price > product['price_min']:
                smile = '📊'

    text_name = f'''{smile} {price}₽ <del>{del_price}₽</del> 🛍 {product["name"]}

🤔Остаток: {product["stock"]}шт

🔥Скидка: {product['sale']}%
{diap_text}

https://www.wb.ru/catalog/{product['id']}/detail.aspx
'''
    # 🧮Средняя
    # цена: {product["average"]}₽
    return text_name