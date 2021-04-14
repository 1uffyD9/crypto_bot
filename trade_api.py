import time
import json
import requests
from random import randrange


class TradeApi:

    def get_change_stats(self, symbol):
        api_list = ['api.binance.com', 'api1.binance.com', 'api2.binance.com', 'api3.binance.com']

        headers = {
            'User-Agent': "Mozilla / 5.0(Windows NT 10.0; Win64; x64; rv: 87.0) Gecko / 20100101 Firefox / 87.0"
        }

        params = {
            'symbol': symbol
        }

        response = requests.get('https://{}/api/v3/ticker/24hr'.format(api_list[randrange(4)]), headers=headers,
                                params=params)

        # take a break if X-MBX-USED-WEIGHT value is getting high
        if int(response.headers['x-mbx-used-weight-1m']) > 15:
            print("[!] x-mbx-used-weight-1m value : {}".format(response.headers['x-mbx-used-weight-1m']))
            time.sleep(20)

        result = json.loads(response.text)
        return {
            'symbol': result['symbol'],
            'priceChangePercent': round(float(result['priceChangePercent']), 2),
            'lastPrice': round(float(result['lastPrice']), 5),
            'princeChangeIntRoundOff': int(float(result['priceChangePercent']))
        }
