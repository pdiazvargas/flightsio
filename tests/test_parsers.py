from flightsio.parsers import (parse_flight_list, parse_flight_routes, parse_destinations)


def test_parse_destinations():
    """
    Given the content of the site that contains all the destinations from a given
    airport. Return a list of airport names and links.
    """

    phx = read_source('phx.html')

    result = parse_destinations(phx)

    assert result == {
        "Calgary": "https://info.flightmapper.net/airport/PHX/YYC",
        "Edmonton": "https://info.flightmapper.net/airport/PHX/YEG",
        "Kelowna": "https://info.flightmapper.net/airport/PHX/YLW",
        "Lester B. Pearson Intl, Toronto": "https://info.flightmapper.net/airport/PHX/YYZ",
        "Pierre Elliott Trudeau, Montreal": "https://info.flightmapper.net/airport/PHX/YUL",
        "Regina": "https://info.flightmapper.net/airport/PHX/YQR",
        "Saskatoon": "https://info.flightmapper.net/airport/PHX/YXE",
        "Vancouver": "https://info.flightmapper.net/airport/PHX/YVR",
        "Winnipeg": "https://info.flightmapper.net/airport/PHX/YWG",
        "Grand Cayman": "https://info.flightmapper.net/airport/PHX/GCM",
        "San Jose": "https://info.flightmapper.net/airport/PHX/SJO",
        "San Salvador": "https://info.flightmapper.net/airport/PHX/SAL",
        "Frankfurt": "https://info.flightmapper.net/airport/PHX/FRA",
        "Benito Juarez Intl, Mexico City": "https://info.flightmapper.net/airport/PHX/MEX",
        "Cancun": "https://info.flightmapper.net/airport/PHX/CUN",
        "Culiacan": "https://info.flightmapper.net/airport/PHX/CUL",
        "Guadalajara": "https://info.flightmapper.net/airport/PHX/GDL",
        "Hermosillo": "https://info.flightmapper.net/airport/PHX/HMO",
        "Ixtapa/Zihuatanejo": "https://info.flightmapper.net/airport/PHX/ZIH",
        "Manzanillo": "https://info.flightmapper.net/airport/PHX/ZLO",
        "Mazatlan": "https://info.flightmapper.net/airport/PHX/MZT",
        "Monterrey": "https://info.flightmapper.net/airport/PHX/MTY",
        "Puerto Vallarta": "https://info.flightmapper.net/airport/PHX/PVR",
        "San Jose del Cabo": "https://info.flightmapper.net/airport/PHX/SJD",
        "Amsterdam": "https://info.flightmapper.net/airport/PHX/AMS",
        "Luis Munoz Marin, San Juan": "https://info.flightmapper.net/airport/PHX/SJU",
        "Heathrow, London": "https://info.flightmapper.net/airport/PHX/LHR",
        "Albany": "https://info.flightmapper.net/airport/PHX/ALB",
        "Albuquerque": "https://info.flightmapper.net/airport/PHX/ABQ",
        "Amarillo": "https://info.flightmapper.net/airport/PHX/AMA",
        "Anchorage": "https://info.flightmapper.net/airport/PHX/ANC",
        "Aspen": "https://info.flightmapper.net/airport/PHX/ASE",
        "Austin": "https://info.flightmapper.net/airport/PHX/AUS",
        "Bakersfield": "https://info.flightmapper.net/airport/PHX/BFL",
        "Baltimore": "https://info.flightmapper.net/airport/PHX/BWI",
        "Birmingham": "https://info.flightmapper.net/airport/PHX/BHM",
        "Boise": "https://info.flightmapper.net/airport/PHX/BOI",
        "Buffalo": "https://info.flightmapper.net/airport/PHX/BUF",
        "Burbank": "https://info.flightmapper.net/airport/PHX/BUR",
        "Charleston": "https://info.flightmapper.net/airport/PHX/CHS",
        "Charlotte": "https://info.flightmapper.net/airport/PHX/CLT",
        "Colorado Springs": "https://info.flightmapper.net/airport/PHX/COS",
        "Corpus Christi": "https://info.flightmapper.net/airport/PHX/CRP",
        "Cortez": "https://info.flightmapper.net/airport/PHX/CEZ",
        "Dallas/Ft. Worth": "https://info.flightmapper.net/airport/PHX/DFW",
        "Denver": "https://info.flightmapper.net/airport/PHX/DEN",
        "Des Moines": "https://info.flightmapper.net/airport/PHX/DSM",
        "Detroit": "https://info.flightmapper.net/airport/PHX/DTW",
        "Dulles, Washington": "https://info.flightmapper.net/airport/PHX/IAD",
        "Durango": "https://info.flightmapper.net/airport/PHX/DRO",
        "Edward L. Logan, Boston": "https://info.flightmapper.net/airport/PHX/BOS",
        "El Paso": "https://info.flightmapper.net/airport/PHX/ELP",
        "Eugene": "https://info.flightmapper.net/airport/PHX/EUG",
        "Flagstaff Pulliam, Grand Canyon": "https://info.flightmapper.net/airport/PHX/FLG",
        "Fort Lauderdale": "https://info.flightmapper.net/airport/PHX/FLL",
        "Fort Myers": "https://info.flightmapper.net/airport/PHX/RSW",
        "Fresno": "https://info.flightmapper.net/airport/PHX/FAT",
        "George Bush, Houston": "https://info.flightmapper.net/airport/PHX/IAH",
        "Grand Junction": "https://info.flightmapper.net/airport/PHX/GJT",
        "Grand Rapids": "https://info.flightmapper.net/airport/PHX/GRR",
        "Greenville/Spartanburg": "https://info.flightmapper.net/airport/PHX/GSP",
        "Harlingen": "https://info.flightmapper.net/airport/PHX/HRL",
        "Hartford": "https://info.flightmapper.net/airport/PHX/BDL",
        "Hartsfield-Jackson, Atlanta": "https://info.flightmapper.net/airport/PHX/ATL",
        "Honolulu": "https://info.flightmapper.net/airport/PHX/HNL",
        "Hopkins, Cleveland": "https://info.flightmapper.net/airport/PHX/CLE",
        "Indianapolis": "https://info.flightmapper.net/airport/PHX/IND",
        "Islip": "https://info.flightmapper.net/airport/PHX/ISP",
        "Jackson": "https://info.flightmapper.net/airport/PHX/JAC",
        "Jacksonville": "https://info.flightmapper.net/airport/PHX/JAX",
        "John F. Kennedy, New York": "https://info.flightmapper.net/airport/PHX/JFK",
        "Kahului": "https://info.flightmapper.net/airport/PHX/OGG",
        "Kansas City": "https://info.flightmapper.net/airport/PHX/MCI",
        "Kona": "https://info.flightmapper.net/airport/PHX/KOA",
        "LaGuardia, New York": "https://info.flightmapper.net/airport/PHX/LGA",
        "Lihue": "https://info.flightmapper.net/airport/PHX/LIH",
        "Little Rock": "https://info.flightmapper.net/airport/PHX/LIT",
        "Long Beach": "https://info.flightmapper.net/airport/PHX/LGB",
        "Los Angeles": "https://info.flightmapper.net/airport/PHX/LAX",
        "Louisville": "https://info.flightmapper.net/airport/PHX/SDF",
        "Love Field, Dallas": "https://info.flightmapper.net/airport/PHX/DAL",
        "Lubbock": "https://info.flightmapper.net/airport/PHX/LBB",
        "Manchester": "https://info.flightmapper.net/airport/PHX/MHT",
        "McCarran, Las Vegas": "https://info.flightmapper.net/airport/PHX/LAS",
        "Medford": "https://info.flightmapper.net/airport/PHX/MFR",
        "Memphis": "https://info.flightmapper.net/airport/PHX/MEM"
    }


def test_parse_flight_list():

    content = read_source('flight_list.html')

    result = parse_flight_list(content)

    assert result == {
        "AA 5950": "https://info.flightmapper.net/flight/American_Airlines_AA_5950",
        "AA 6003": "https://info.flightmapper.net/flight/American_Airlines_AA_6003",
        "WN 55": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_55",
        "WN 347": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_347",
        "WN 379": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_379",
        "WN 392": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_392",
        "WN 543": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_543",
        "WN 736": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_736",
        "WN 783": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_783",
        "WN 913": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_913",
        "WN 1078": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_1078",
        "WN 1291": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_1291",
        "WN 1353": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_1353",
        "WN 1423": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_1423",
        "WN 1439": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_1439",
        "WN 1441": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_1441",
        "WN 1552": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_1552",
        "WN 1701": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_1701",
        "WN 1989": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_1989",
        "WN 1992": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_1992",
        "WN 2004": "https://info.flightmapper.net/flight/Southwest_Airlines_WN_2004",
    }


def test_parse_flight_routes():

    url = 'findme.com'
    flight = 'flight'
    content = read_source('single_flight.html')

    result = parse_flight_routes(flight, url, content)

    assert result == [
        {'flight': flight, 'frequency': 'Daily', 'departure': '08:35', 'from': 'Sky Harbor, Phoenix (PHX) 4', 'arrival': '12:51', 'to': 'Oklahoma City (OKC) ', 'flight': 'AA 5950', 'other': 'Non-stop Canadair CRJ 900 (CR9) 2:16', 'duration': 'Effective 2018-04-03 through 2018-05-03', 'url': url},
        {'flight': flight, 'frequency': 'Daily', 'departure': '12:10', 'from': 'Sky Harbor, Phoenix (PHX) 4', 'arrival': '16:18', 'to': 'Oklahoma City (OKC) ', 'flight': 'AA 5950', 'other': 'Non-stop Canadair CRJ 900 (CR9) 2:08', 'duration': 'Effective 2018-05-04 through 2018-06-06', 'url': url},
        {'flight': flight, 'frequency': 'Daily', 'departure': '13:21', 'from': 'Oklahoma City (OKC)', 'arrival': '13:55', 'to': 'Sky Harbor, Phoenix (PHX) 4', 'flight': 'AA 5950', 'other': 'Non-stop Canadair CRJ 900 (CR9) 2:34', 'duration': 'Effective 2018-04-03 through 2018-05-03', 'url': url},
        {'flight': flight, 'frequency': 'Daily', 'departure': '18:46', 'from': 'Sky Harbor, Phoenix (PHX) 4', 'arrival': '21:01', 'to': 'El Paso (ELP) ', 'flight': 'AA 5950', 'other': 'Non-stop Canadair CRJ 900 (CR9) 1:15', 'duration': '', 'url': url},
    ]


def read_source(name):

    with open(f'./html/{name}', 'r') as f:
        return f.read()
