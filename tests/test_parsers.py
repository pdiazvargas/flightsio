from flightsio.parsers import parse_flight_list, parse_flight_routes


def test_parse_flight_list():

    with open('./html/flight_list.html', 'r') as f:
        content = f.read()

    result = parse_flight_list(content)

    assert result == {
        "AA 5950": "http://info.flightmapper.net/flight/American_Airlines_AA_5950",
        "AA 6003": "http://info.flightmapper.net/flight/American_Airlines_AA_6003",
        "WN 55": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_55",
        "WN 347": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_347",
        "WN 379": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_379",
        "WN 392": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_392",
        "WN 543": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_543",
        "WN 736": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_736",
        "WN 783": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_783",
        "WN 913": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_913",
        "WN 1078": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_1078",
        "WN 1291": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_1291",
        "WN 1353": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_1353",
        "WN 1423": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_1423",
        "WN 1439": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_1439",
        "WN 1441": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_1441",
        "WN 1552": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_1552",
        "WN 1701": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_1701",
        "WN 1989": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_1989",
        "WN 1992": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_1992",
        "WN 2004": "http://info.flightmapper.net/flight/Southwest_Airlines_WN_2004",
    }


def test_parse_flight_routes():

    with open('./html/single_flight.html', 'r') as f:
        content = f.read()

    result = parse_flight_routes(content)

    assert result == [
        {'frequency': 'Daily ', 'departure': '08:35 ', 'from': 'Sky Harbor, Phoenix (PHX) 4 ', 'arrival': '12:51 ', 'to': 'Oklahoma City (OKC) ', 'flight': 'AA 5950', 'other': 'Non-stop Canadair CRJ 900 (CR9) 2:16', 'duration': 'Effective 2018-04-03 through 2018-05-03'},
        {'frequency': 'Daily ', 'departure': '12:10 ', 'from': 'Sky Harbor, Phoenix (PHX) 4 ', 'arrival': '16:18 ', 'to': 'Oklahoma City (OKC) ', 'flight': 'AA 5950', 'other': 'Non-stop Canadair CRJ 900 (CR9) 2:08', 'duration': 'Effective 2018-05-04 through 2018-06-06'},
        {'frequency': 'Daily ', 'departure': '13:21 ', 'from': 'Oklahoma City (OKC)  ', 'arrival': '13:55 ', 'to': 'Sky Harbor, Phoenix (PHX) 4', 'flight': 'AA 5950', 'other': 'Non-stop Canadair CRJ 900 (CR9) 2:34', 'duration': 'Effective 2018-04-03 through 2018-05-03'},
        {'frequency': 'Daily ', 'departure': '18:46 ', 'from': 'Sky Harbor, Phoenix (PHX) 4 ', 'arrival': '21:01 ', 'to': 'El Paso (ELP) ', 'flight': 'AA 5950', 'other': 'Non-stop Canadair CRJ 900 (CR9) 1:15', 'duration': 'Valid until 2018-04-02'}
    ]
