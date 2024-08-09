import httpx
from app.pair_mapping import PAIR_MAPPING


class BinanceClient:
    def __init__(self):
        self.api_url = "https://api.binance.com/api/v3/ticker/bookTicker"
        self.cached_prices = {}

    async def update_prices(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.api_url)
            data = response.json()
            prices = {}
            for item in data:
                symbol = item['symbol']
                bid_price = float(item['bidPrice'])
                ask_price = float(item['askPrice'])
                avg_price = (bid_price + ask_price) / 2
                prices[symbol] = {
                    'bid': bid_price,
                    'ask': ask_price,
                    'average': avg_price
                }
            self.cached_prices = prices

    def get_cached_prices(self):
        return self.cached_prices


class KrakenClient:
    def __init__(self):
        self.api_url_ticker = "https://api.kraken.com/0/public/Ticker"
        self.api_url_pairs = "https://api.kraken.com/0/public/AssetPairs"
        self.cached_prices = {}

    async def update_prices(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.api_url_pairs)
            pairs = [pair for pair in response.json()["result"].keys()]
            response = await client.get(self.api_url_ticker, params={"pair": ",".join(pairs)})
            data = response.json()["result"]
            prices = {}
            for pair, value in data.items():
                normalized_pair = self.normalize_pair(pair)
                bid_price = float(value['b'][0])
                ask_price = float(value['a'][0])
                avg_price = (bid_price + ask_price) / 2
                prices[normalized_pair] = {
                    'bid': bid_price,
                    'ask': ask_price,
                    'average': avg_price
                }
            self.cached_prices = prices

    def get_cached_prices(self):
        return {PAIR_MAPPING.get(pair, pair): price_data for pair, price_data in self.cached_prices.items()}

    def normalize_pair(self, pair):
        return PAIR_MAPPING.get(pair, pair)
