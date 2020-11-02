from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com//v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '1',
    'market_cap_max': '0',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '43cc8854-523c-49d3-a25c-5f2209fca170',
}


def getCMCRank(mc):
    session = Session()
    session.headers.update(headers)
    try:
        parameters['market_cap_max'] = int(mc)
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data['data'][0]['cmc_rank']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return 999
