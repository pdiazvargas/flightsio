import time
import json
import requests

from itertools import cycle
from bs4 import BeautifulSoup

from flightsio.proxies import ProxyRequest
from flightsio.parsers import (parse_flight_list, parse_flight_routes)
from flightsio.constants import MAX_RETRIES, SLEEP_INTERVALS, CAPTCHA


def run(source_url):

    # The object used to get a set of IP addressed. These will be used as a proxy
    # when making a request to the flight endpoint.
    proxy_request = ProxyRequest()

    # Make a request to the flights endpoint to get the routes available between
    # the two airports.
    response = proxy_request.get(source_url)

    if response.status_code != requests.codes.ok:
        print(f'Unable to make a request to: "{source_url}"')
        print(response.content)
        return

    flights = parse_flight_list(response.content)
    sleep_interval = cycle(SLEEP_INTERVALS)

    # Iterate over the set of routes, make a request to each url and write the
    # output in json format.
    for flight, flight_url in flights.items():
        sleep_time = next(sleep_interval)

        print(f'"{flight}:15" "{proxy_request.ip}:20" sleeping for {sleep_time} secs')
        response = proxy_request.get(flight_url)

        if response.status_code != requests.codes.ok:
            import pdb; pdb.set_trace()
            print('Unable to make request. Response was:\n')
            print(response.content.decode())
            continue

        flight_routes = parse_flight_routes(response.content.decode())
        writer(flight, flight_routes)

        sleep_time = next(sleep_interval)
        time.sleep(sleep_time)


def writer(flight, routes):

    with open(f'./output/{flight}.json', 'w') as f:
        f.write(json.dumps(routes, indent=4))

if __name__ == '__main__':
    source_url = 'http://info.flightmapper.net/airport/PHX/OKC'
    run(source_url)
