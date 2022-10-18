from fake_useragent import UserAgent
from config import proxies_file
import requests
from random import choice




def get_html(url, params=None):
    ua = UserAgent()
    proxies = open(proxies_file).read().split('\n')
    useragent = {'User-Agent': ua.random}
    proxy = {'http': 'http://' + choice(proxies)}
    r = requests.get(url.strip(), params=params, headers=useragent)
    return r.text