# flightsio

## Run the script

First step is to install the requirements for the project. These are defined in
the requirements.txt file.

    $ pip install -r requirements.txt

## Command line

To dynamically invoke the functions available in flightsio, you can use the provide
command line utility. To install the utility run the following command:

    $ pip install -e .

After executing the installer you should have access to the `fio` command line.
Calling `fio` in the command line should give you an output similar to:

    $ fio
    Usage: fio [OPTIONS] COMMAND [ARGS]...

    An empty click group, required in order to bundle the other commands.

    Options:
    --help  Show this message and exit.

    Commands:
    all-routes    Reads the entire destination list of of the given airport...
    destinations  Reads the entire destination list of of the given airport...
    routes        Reads the route list between a source airport and a...

## Invoke actions
After installing the command line utility, you have access to the commands provided
by fio. To explore the inputs required by each command you can use `--help` argument.

    $ fio destinations --help
    Usage: fio destinations [OPTIONS]

    Reads the entire destination list of of the given airport returns the name
    of the airport and url associated with it. Sample usage: fio destinations
    --from-airport PHX

    Options:
    -a, --from-airport TEXT  The three letter code of the source airport. I.e.
                            PHX
    -v, --verbosity LVL      Either CRITICAL, ERROR, WARNING, INFO or DEBUG
    --help                   Show this message and exit.

    A sample usage of the destinations command requires the --from-airport argument
    to have the letter code of an airport. Invoking it looks like:

    $ fio destinations --from-airport phx
    {
        "Sioux Falls": "https://info.flightmapper.net/airport/PHX/FSD",
        "Jacksonville": "https://info.flightmapper.net/airport/PHX/JAX",
        "Manzanillo": "https://info.flightmapper.net/airport/PHX/ZLO",
        ...
        "Detroit": "https://info.flightmapper.net/airport/PHX/DTW",
        "New Orleans": "https://info.flightmapper.net/airport/PHX/MSY"
    }

## Unit Tests

The project has a very basic set of unit tests used to develop the logic in the
parsers. The unit tests read a given sample html file and then parse the contents
of the file. To run the unit tests:

    $ python -m pytest
