import time
import json
import requests

from itertools import cycle
from bs4 import BeautifulSoup

from flightsio.proxies import SslProxyGenerator
from flightsio.parsers import (parse_flight_list, parse_flight_routes)
from flightsio.constants import MAX_RETRIES, SLEEP_INTERVALS, CAPTCHA


def run(source_url):

    # The object used to get a set of IP addressed. These will be used as a proxy
    # when making a request to the flight endpoint.
    proxy_gen = SslProxyGenerator()

    # Make a request to the flights endpoint to get the routes available between
    # the two airports.
    response = retry_request(proxy_gen, source_url, MAX_RETRIES)

    if response.status_code != requests.codes.ok:
        print(f'Unable to make a request to: "{source_url}"')
        print(response.content)
        return

    flights = parse_flight_list(response.content)
    sleep_interval = cycle(SLEEP_INTERVALS)

    # Iterate over the set of routes, make a request to each url and write the
    # output in json format.
    for flight, flight_url in flights.items():
        print(f'Getting routes for "{flight}".')
        response = retry_request(proxy_gen, flight_url)

        if response.status_code != requests.codes.ok:
            import pdb; pdb.set_trace()
            print('Unable to make request. Response was:\n')
            print(response.content.decode())
            continue

        flight_routes = parse_flight_routes(response.content.decode())
        writer(flight, flight_routes)

        https_proxy['https'] = proxy_gen.get_proxy()

        sleep_time = next(sleep_interval)
        print(f'Sleeping for {sleep_time} secs')
        time.sleep(sleep_time)


def retry_request(proxy_gen, url, retries=MAX_RETRIES):

    # Make a request to the flights endpoint to get the routes available between
    # the two airports.
    new_ip = proxy_gen.get_proxy()
    response = requests.get(url, proxies={'https': new_ip})

    if retries == 0:
        print(f'Exhausted the number of retries for "{url}"')
        return response

    if response.status_code == requests.codes.forbidden:
        print(f'Found catpcha, retrying with new IP {new_ip}')
        time.sleep(1)
        return retry_request(proxy_gen, url, retries - 1)

    return response


def writer(flight, routes):

    with open(f'./output/{flight}.json', 'w') as f:
        f.write(json.dumps(routes, indent=4))

if __name__ == '__main__':
    source_url = 'http://info.flightmapper.net/airport/PHX/OKC'
    run(source_url)
