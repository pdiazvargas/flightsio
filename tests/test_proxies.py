import requests
from flightsio import proxies, constants
from unittest.mock import MagicMock


# For testing purposes set the number of seconds to wait between retries to 0.
# there's no reason to wait while testing.
proxies.DEFAULT_RETRY_INTERVAL = 0


def test_proxy_request_200_status_code(mocker):

    mock_proxy_gen, mock_get = setup_mocks(mocker, requests.codes.ok)

    proxy_request = proxies.ProxyRequest()

    target_url = 'https://find.me'
    response = proxy_request.get(target_url)

    mock_get.assert_called_once()


def test_proxy_request_200_includes_http_arg(mocker):

    mock_proxy_gen, mock_get = setup_mocks(mocker, requests.codes.ok)

    proxy_request = proxies.ProxyRequest()
    proxy_request._current_ip = '94.45.153.229:60784'

    target_url = 'https://find.me'
    response = proxy_request.get(target_url)

    args, kwargs = mock_get.call_args
    assert kwargs['proxies']['http'] == proxy_request._current_ip


def test_proxy_request_200_includes_user_agen(mocker):

    mock_proxy_gen, mock_get = setup_mocks(mocker, requests.codes.ok)

    mock_user_agent = mocker.patch('flightsio.proxies.ua')

    proxy_request = proxies.ProxyRequest()
    proxy_request._current_ip = '94.45.153.229:60784'

    target_url = 'https://find.me'
    response = proxy_request.get(target_url)

    args, kwargs = mock_get.call_args
    assert kwargs['headers']['User-Agent'] == mock_user_agent.random


def test_proxy_request_403_retries_request(mocker):
    """
    A 403 forbidden, means that the site has completely block an ip. The url should
    be retried a specific number of times before giving up.
    """

    mock_proxy_gen, mock_get = setup_mocks(mocker, requests.codes.forbidden)

    proxy_request = proxies.ProxyRequest()

    target_url = 'https://find.me'
    response = proxy_request.get(target_url, 3)

    # The total call count should be the max number of retries, plus the original.
    assert mock_get.call_count == 4


def test_proxy_request_403_generates_new_ip(mocker):
    """
    With 403 forbidden, generate a new IP for the subsequent request.
    """

    mock_proxy_gen, mock_get = setup_mocks(mocker, requests.codes.forbidden)

    proxy_request = proxies.ProxyRequest()
    proxy_request._reset_ip = MagicMock()

    target_url = 'https://find.me'
    response = proxy_request.get(target_url, 3)

    # The number of ips generated should equal the max number of retires.
    assert proxy_request._reset_ip.call_count == 3


def test_proxy_request_reset_ip(mocker):
    """
    Validates that a new ip address is requested when the reset_ip method is invoked.
    This is an internal method and it will be called whenever a request responds with
    a 403 status code.
    """

    new_ip = '165.90.66.230:58667'
    mock_proxy_gen = mocker.patch('flightsio.proxies.SslIpGenerator')
    mock_proxy_gen.return_value.get_ip = MagicMock(return_value=new_ip)

    request = proxies.ProxyRequest()
    request._current_ip = 'old:ip'

    request._reset_ip()

    assert request._current_ip == new_ip


def setup_mocks(mocker, status_code):

    mock_proxy_gen = mocker.patch('flightsio.proxies.SslIpGenerator')
    mock_get = mocker.patch('flightsio.proxies.requests.get')
    mock_get.return_value = MagicMock(status_code=status_code)

    return (mock_proxy_gen, mock_get)


def test_proxy_gen(mocker):

    mock_content = read_artifact('sample_proxies.html')
    mock_get = mocker.patch('flightsio.proxies.requests.get')
    mock_get.return_value = MagicMock(status_code=requests.codes.ok, content=mock_content)

    proxy_generator = proxies.SslIpGenerator()
    proxy_generator.load_proxies()

    ips = set([proxy_generator.get_ip() for i in range(100)])
    # The first three ip addresses in the sample proxies file are in the set of all ips
    assert {'87.249.19.154:48996', '1.20.100.183:40424', '125.26.108.12:30540'} < ips


def read_artifact(name):

    with open(f'./html/{name}', 'r') as f:
        return f.read()