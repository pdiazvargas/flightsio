import random
from bs4 import BeautifulSoup

from flightsio.constants import ROUTE_FIELDS


def parse_destinations(destinations_html):

    soup = BeautifulSoup(destinations_html, 'html.parser')
    links = [link for link in soup.find_all('a') if '/airport/' in link.get('href')]
    random.shuffle(links)

    return {
        link.text: 'https://info.flightmapper.net' + link.get('href')
        for link in links
    }


def parse_flight_list(flights_html):
    """
    Parse the available flight information from a given set of destinations. The html page
    will have a given set of links, we're only concerned with the links that point to a
    given flight. Extract those along with the name of the flight.

    Example of page this function can consume.
    http://info.flightmapper.net/airport/PHX/OKC

    :params flights_html: The html page containing a set of flights between two destinations.
    """

    soup = BeautifulSoup(flights_html, 'html.parser')

    return {
        link.text: 'https://info.flightmapper.net' + link.get('href')
        for link in soup.find_all('a') if '/flight/' in link.get('href')
    }


def parse_flight_routes(flight, flight_url, flight_html):

    soup = BeautifulSoup(flight_html, 'html.parser')

    def get_flight_info(flight_rec):
        data = flight_rec.text.strip().split('\n')

        if len(data) < len(ROUTE_FIELDS):
            data.append('')

        info = {field: data[i] for i, field in enumerate(ROUTE_FIELDS)}
        return {'flight': flight, **info, 'url': flight_url}

    return [get_flight_info(rec) for rec in soup.find_all('tr') if len(rec.find_all('td'))]
