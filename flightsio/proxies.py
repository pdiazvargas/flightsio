import time
import random
import requests

from flightsio.constants import MAX_RETRIES
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

        random.shuffle(self._proxies)
        self._proxy_gen = cycle(self._proxies)

    # Retrieve a random index proxy (we need the index to delete it if not working)
    def get_ip(self):
        return next(self._proxy_gen)


class ProxyRequest:

    REQUEST_MAX_COUNT = 10

    def __init__(self):
        self._proxy_gen = SslProxyGenerator()
        self._reset_ip()

    @property
    def ip(self):
        return self._current_ip

    def _get_ip(self):

        if self._request_count == self.REQUEST_MAX_COUNT:
            print(f'Used "{self._current_ip}"" {self._request_count} times.')
            self._reset_ip()

        self._request_count += 1
        return self._current_ip

    def _reset_ip(self):
        self._request_count = 0
        self._current_ip = self._proxy_gen.get_ip()

    def get(self, url, retries=MAX_RETRIES):

        # Make a request to the flights endpoint to get the routes available between
        # the two airports.
        ip_addr = self._get_ip()
        response = requests.get(url, proxies={'https': ip_addr})

        if retries == 0:
            print(f'Exhausted the number of retries for "{url}"')
            return response

        if response.status_code == requests.codes.forbidden:
            print(f'Found catpcha, retrying with new IP {ip_addr}. Sleeping for a while...')
            self._reset_ip()
            time.sleep(5)
            return self.get(url, retries - 1)

        return response

if __name__ == '__main__':
    import requests

    p = SslProxyGenerator()
    print(p.get_ip())
