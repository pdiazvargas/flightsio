import os
import time
import json
import click
import click_log
import logging

from flightsio.scraper import FlightScraper

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.group()
def main():
    """
    An empty click group, required in order to bundle the other commands.
    """
    pass


@main.command(help="""Reads the entire destination list of of the given airport
                    returns the name of the airport and url associated with it.
                    Sample usage: fio destinations --from-airport PHX""")
@click.option('--from-airport', '-a', help='The three letter code of the source airport. I.e. PHX')
@click_log.simple_verbosity_option(logger)
def destinations(from_airport):

    if not from_airport:
        logger.error('Unable to get destinations without an aiport code. Use fio destinations --help')
        return

    destinations = FlightScraper().get_destinations(from_airport.upper())
    logger.info(json.dumps(destinations, indent=4))


@main.command(help="""Reads the entire destination list of of the given airport and crawls
                      each destination to obtain the list of routes. The output files will
                      stored in the given folder. Sample usage:
                      fio all-routes --from-airport PHX --output ./out
                    """)
@click.option('--from-airport', '-a', help='The three letter code of the source airport. I.e. PHX')
@click.option('--output', '-o', help='The path used to write the parsed routes.', default='./output')
@click_log.simple_verbosity_option(logger)
def all_routes(from_airport, output):

    if not from_airport:
        logger.error('Unable to get all routes without an aiport code. Use fio all_routes --help')
        return

    airport = from_airport.upper()

    scraper = FlightScraper()
    airport_path = os.path.join(output, airport)
    logger.info(f'Creating {airport_path}')
    os.makedirs(airport_path, exist_ok=True)

    for destination, routes in scraper.get_routes(airport):
        write_csv(airport_path, destination, routes)


@main.command(help="""Reads the route list between a source airport and a destination airport and
                      writes the result in the output folder. Sample usage:
                      fio routes --from-airport PHX --to-airport OKC --output ./out
                    """)
@click.option('--from-airport', '-a', help='The three letter code of the source airport. I.e. PHX')
@click.option('--to-airport', '-b', help='The three letter code of the destination airport. I.e. OKC')
@click.option('--output', '-o', help='The path used to write the parsed routes.', default='./output')
@click_log.simple_verbosity_option(logger)
def routes(from_airport, to_airport, output):

    if not from_airport or not to_airport:
        logger.error('Unable to get routes without aiport codes. Use fio routes --help')
        return

    airport = from_airport.upper()

    scraper = FlightScraper()
    route_path = os.path.join(output, 'single_routes')
    logger.info(f'Creating {route_path}')
    os.makedirs(route_path, exist_ok=True)

    destination_link = scraper.get_fm_link(from_airport, to_airport)
    name, routes = scraper.get_flight_foutes(to_airport, destination_link)

    write_csv(route_path, f'{from_airport}_{to_airport}', routes)


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
    main()
