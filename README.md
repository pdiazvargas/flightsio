# flightsio

## Run the script

First step is to install the requirements for the project. These are defined in
the requirements.txt file.

> pip install -r requirements.txt

The `runner.py` file has a sample run using the components of the flights.io
engine. The runner will parse a given set of routes from the given url endpoint
and then it will retrieve the route information for each flight. The output
will be writen to an `output` directory.

> python runner.py

## Unit Tests

The project has a very basic set of unit tests used to develop the logic in the
parsers. The unit tests read a given sample html file and then parse the contents
of the file. To run the unit tests:

> python -m pytest
