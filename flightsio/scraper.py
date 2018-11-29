import os
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

    def get_fm_link(self, from_airport, to_airport):
        return os.path.join(self.BASE_URL, from_airport, to_airport)

    def get_destinations(self, source_airport):

        airport_url = f'{self.BASE_URL}/{source_airport}'
        response = self.proxy_request.get(airport_url)

        if response.status_code != requests.codes.ok:
            print(f'Unable to get destinations for: "{airport_url}". Response content was:')
            print(response.content)
            return

        return parse_destinations(response.content)

    def get_routes(self, source_airport):

        airport_url = f'{self.BASE_URL}/{source_airport}'
        response = self.proxy_request.get(airport_url)

        if response.status_code != requests.codes.ok:
            print(f'Unable to make a request to: "{airport_url}"')
            print(response.content)
            return

        destinations = parse_destinations(response.content)
        for destination, destination_url in destinations.items():
            yield self.get_flight_foutes(destination, destination_url)

    def get_flight_foutes(self, destination, destination_url):

        # Make a request to the flights endpoint to get the routes available between
        # the two airports.
        response = self.proxy_request.get(destination_url)

        if response.status_code != requests.codes.ok:
            print(f'Unable to make a request to: "{destination_url}"')
            print(response.content)
            return

        flights = parse_flight_list(response.content)
        sleep_interval = cycle(SLEEP_INTERVALS)
        print(f'{destination_url} has {len(flights)} flights')

        all_routes = []
        start = time.time()
        # Iterate over the set of routes, make a request to each url and write the
        # output in json format.
        for flight, flight_url in flights.items():
            sleep_time = next(sleep_interval)

            print(f'{flight:10} {self.proxy_request.ip:20} sleeping for {sleep_time} secs')
            response = self.proxy_request.get(flight_url)

            if response.status_code != requests.codes.ok:
                # After making several requests to the fligh_url, the response did not succeed.
                # Need to skip this flight.
                # Todo: Maybe keep a list of the links that have not completed in this way
                # for future processing.
                print(f'Unable to make request to: {flight_url}. This flight has bee skipped.')
                continue

            flight_routes = parse_flight_routes(flight, flight_url, response.content.decode())
            all_routes.extend(flight_routes)

            sleep_time = next(sleep_interval)
            time.sleep(sleep_time)

        diff = time.time() - start
        print(f'Parsing completed in {diff:.2f} secs\n')

        # Get the airport code for the destination from the url.
        destination_code = destination_url.rsplit('/', 1)[1]
        # Simplify the name of the destination
        new_name = destination.title().replace(' ', '').replace(',', '').replace('/', '')
        return (f'{destination_code}_{new_name}', all_routes)
