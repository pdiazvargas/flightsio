import random
import requests

from itertools import cycle
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()  # From here we generate a random user agent


class SslProxyGenerator:

    def __init__(self):
        self._load_proxies()

    def _load_proxies(self):
        # Retrieve latest proxies
        proxies_doc = requests.get('https://www.sslproxies.org/', headers={'User-Agent': ua.random})

        soup = BeautifulSoup(proxies_doc.content, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')

        # Strips the ip and port from the sslproxies table.
        # After processing the array will look like:
        # ['10.10.10.10:8080', '11.10.10.10:8090', ...]
        self._proxies = [
            row.find_all('td')[0].string + ':' + row.find_all('td')[1].string
            for row in proxies_table.tbody.find_all('tr')
        ]

        self._proxy_gen = cycle(self._proxies)

    # Retrieve a random index proxy (we need the index to delete it if not working)
    def get_proxy(self):
        return next(self._proxy_gen)


if __name__ == '__main__':
    import requests

    p = SslProxyGenerator()
    print(p.get_proxy())
