import requests
import json
from config import TOKEN

class APIException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{base}")
            data = json.loads(response.text)
            if quote.upper() not in data["rates"]:
                raise APIException(f"Invalid currency: {quote}")
            exchange_rate = data["rates"][quote.upper()]
            result = exchange_rate * amount
            return result
        except Exception as e:
            raise APIException(str(e))