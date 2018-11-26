import time
import json
import requests

from itertools import cycle
from bs4 import BeautifulSoup

from flightsio.proxies import ProxyRequest
from flightsio.parsers import (parse_flight_list, parse_flight_routes, parse_destinations)
from flightsio.constants import MAX_RETRIES, SLEEP_INTERVALS


# recaptcha-checkbox-checkmark

class FlightScraper:
    BASE_URL = 'https://info.flightmapper.net/airport'

    def __init__(self):
        # The object used to get a set of IP addressed. These will be used as a proxy
        # when making a request to the flight endpoint.
        self.proxy_request = ProxyRequest()

    def get_routes(self, source_airport):

        airport_url = f'{self.BASE_URL}/{source_airport}'
        response = self.proxy_request.get(airport_url)

        if response.status_code != requests.codes.ok:
            print(f'Unable to make a request to: "{airport_url}"')
            print(response.content)
            return

        destinations = parse_destinations(response.content)

        for destination, destination_url in destinations.items():

            if 'IAH' in destination_url or 'MTY' in destination_url or 'TEX' in destination_url:
                continue

            yield self.get_flight_foutes(destination, destination_url)

    def get_flight_foutes(self, destination, destination_url):

        print(f'Parsing "{destination}"')
        # Make a request to the flights endpoint to get the routes available between
        # the two airports.
        response = self.proxy_request.get(destination_url)

        if response.status_code != requests.codes.ok:
            print(f'Unable to make a request to: "{source_url}"')
            print(response.content)
            return

        flights = parse_flight_list(response.content)
        sleep_interval = cycle(SLEEP_INTERVALS)

        all_routes = []
        # Iterate over the set of routes, make a request to each url and write the
        # output in json format.
        for flight, flight_url in flights.items():
            sleep_time = next(sleep_interval)

            print(f'{flight:10} {self.proxy_request.ip:20} sleeping for {sleep_time} secs')
            response = self.proxy_request.get(flight_url)

            if response.status_code != requests.codes.ok:
                import pdb; pdb.set_trace()
                print(f'Unable to make request to: {flight_url}')

            flight_routes = parse_flight_routes(flight, flight_url, response.content.decode())
            all_routes.extend(flight_routes)

            sleep_time = next(sleep_interval)
            time.sleep(sleep_time)

        # Get the airport code for the destination from the url.
        destination_code = destination_url.rsplit('/', 1)[1]
        # Simplify the name of the destination
        new_name = destination.title().replace(' ', '').replace(',', '').replace('/', '')
        return (f'{destination_code}_{new_name}', all_routes)
