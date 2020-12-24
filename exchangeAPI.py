import requests
import myWeb3
import util

api_url = 'https://api.anyswap.exchange/ticker'


class VOLRecord:
    def __init__(self, base_id, quote_id, last_price, base_volume, quote_volume, isFrozen, bnbPrice, fsnPrice):
        self.base_id = base_id
        self.quote_id = quote_id
        self.last_price = last_price
        self.base_volume = base_volume
        self.quote_volume = quote_volume
        self.isFrozn = isFrozen
        self.name = self.base_id + '-' + self.quote_id.replace('_', '').replace(self.base_id, '')
        if self.base_id == 'BNB':
            self.price = bnbPrice
        elif self.base_id == 'FSN':
            self.price = fsnPrice
        elif 'USD' in self.base_id:
            self.price = 1
        else:
            raise Exception(f'Unrecognized base {self.base_id}')
        self.vol = float(self.quote_volume) * self.price
        return

    def __str__(self):
        return util.build_href('pair', self.name, self.name.ljust(10)) + f'${self.vol:,.0f}'


def getVOL():
    try:
        result = []
        resp = requests.get(api_url)
        fsnPrice = myWeb3.getPrice('FSN')
        bnbPrice = myWeb3.getPrice('BNB')
        for lp in resp.json().items():
            row = lp[1]
            rec = VOLRecord(row['base_id'], row['quote_id'], row['last_price'], row['base_volume'], row['quote_volume'], row['isFrozen'], bnbPrice, fsnPrice)
            result.append(rec)
        return result
    except Exception as error:
        util.error()
        print(error)
    return
