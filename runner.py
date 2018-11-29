import time
import json
import os

from flightsio.scraper import FlightScraper


def run(source_airport):

    scraper = FlightScraper()
    airport_path = os.path.join('.', 'output', source_airport)

    for destination, routes in scraper.get_routes(source_airport):
        os.makedirs(airport_path, exist_ok=True)
        write_csv(airport_path, destination, routes)


def write_csv(path, destination, routes):

    if not len(routes):
        print(f'{destination} has no routes. Nothing to write.')
        return

    header = ','.join(routes[0])
    with open(os.path.join(path, f'{destination}.csv'), 'w') as f:
        f.write(header + '\n')
        for route in routes:
            row = ','.join((v.strip().replace(',', ' ') for v in route.values()))
            f.write(row + '\n')


def write_json(destination_path, flight, routes):

    with open(os.path.join(destination_path, f'{flight}.json'), 'w') as f:
        f.write(json.dumps(routes, indent=4))


if __name__ == '__main__':
    run('PHX')
