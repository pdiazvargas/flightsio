import time
import json
import requests

from flightsio.proxies import SslProxyGenerator
from flightsio.parsers import (parse_flight_list, parse_flight_routes)
from bs4 import BeautifulSoup

CAPTCHA = 'The website has detected requests which look like automated'


def run(source_url):

    proxy_gen = SslProxyGenerator()
    https_proxy = {'https': proxy_gen.get_proxy()}

    response = requests.get(source_url, proxies=https_proxy)

    if response.status_code != requests.codes.ok:
        print(f'Unable to make a request to: "{source_url}"')
        print(response.content)
        return

    flights = parse_flight_list(response.content)

    for flight, flight_url in flights.items():
        print(f'Parsing the routes for "{flight}"')
        response = requests.get(flight_url, proxies=https_proxy)

        if response.status_code != requests.codes.ok:
            import pdb; pdb.set_trace()
        if CAPTCHA in response.content.decode():
            import pdb; pdb.set_trace()

        flight_routes = parse_flight_routes(response.content.decode())
        writer(flight, flight_routes)

        https_proxy['https'] = proxy_gen.get_proxy()


def writer(flight, routes):

    with open(f'./output/{flight}.json', 'w') as f:
        f.write(json.dumps(routes, indent=4))

if __name__ == '__main__':
    source_url = 'http://info.flightmapper.net/airport/PHX/OKC'
    run(source_url)
