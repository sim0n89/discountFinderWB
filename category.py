import requests
import json
from config import except_men_items
import gc
import random
import pprint


class Category():
    link = 'https://static.wbstatic.net/data/main-menu-ru-ru.json'

    def get_categories(self):
        r = requests.get(self.link)
        menu = json.loads(r.text)
        return (menu)

    def get_category_links(self):
        menu = self.get_categories()
        links = []
        for item in menu:
            if item['id'] in except_men_items:
                for child in item['childs']:
                    if 'childs' in child:
                        for ch in child['childs']:
                            link = {
                                'shard': ch['shard'],
                                'query': ch['query']
                            }

                            links.append(link)
                    else:
                        for child in item['childs']:
                            link = {
                                'shard': child['shard'],
                                'query': child['query']
                            }

                            links.append(link)

        random.shuffle(links)
        return links
