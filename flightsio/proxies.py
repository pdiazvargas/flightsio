import time
import random
import requests

from flightsio.constants import MAX_RETRIES, DEFAULT_RETRY_INTERVAL, CAPTCHA
from itertools import cycle
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()  # From here we generate a random user agent


class SslIpGenerator:
    # Inspired by: https://codelike.pro/create-a-crawler-with-rotating-ip-proxy-in-python/

    def load_proxies(self):
        # Retrieve latest proxies
        proxies_doc = requests.get('https://www.sslproxies.org/', headers={'User-Agent': ua.random})

        soup = BeautifulSoup(proxies_doc.content, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')

        # Strips the ip and port from the sslproxies table.
        # After processing the array will look like:
        # ['10.10.10.10:8080', '11.10.10.10:8090', ...]
        proxies = [
            row.find_all('td')[0].string + ':' + row.find_all('td')[1].string
            for row in proxies_table.tbody.find_all('tr')
        ]

        random.shuffle(proxies)
        self._proxy_gen = cycle(proxies)

    # Retrieve a random index proxy (we need the index to delete it if not working)
    def get_ip(self):
        return next(self._proxy_gen)


class ProxyRequest:

    def __init__(self):
        self._proxy_gen = SslIpGenerator()
        self._proxy_gen.load_proxies()
        self._reset_ip()

    @property
    def ip(self):
        return self._current_ip

    def _reset_ip(self):
        """
        Resets the internal request counter and requests a brand new IP address.
        """
        self._request_count = 0
        self._current_ip = self._proxy_gen.get_ip()

    def get(self, url, retries=MAX_RETRIES):

        # Make a request to the flights endpoint to get the routes available between
        # the two airports.
        ip_addr = self.ip
        self._request_count += 1
        response = requests.get(url, headers={'User-Agent': ua.random}, proxies={'http': ip_addr})

        if retries == 0:
            print(f'Exhausted the number of retries for "{url}"')
            return response

        if CAPTCHA in response.content.decode():
            print(f'Captcha found on {url}')
            import ipdb; ipdb.set_trace()
            self._reset_ip()
            return self.get(url, retries - 1)

        if response.status_code == requests.codes.forbidden:
            print(f'Used "{self._current_ip}" {self._request_count} times. Generating new IP.')
            self._reset_ip()
            time.sleep(DEFAULT_RETRY_INTERVAL)
            return self.get(url, retries - 1)

        return response
