import requests
import json
from config import keys

class ConvertionExeption(Exception):
    pass

class CyrrencyConverter:
    @staticmethod
    def get_price(quote = str, base = str, amount = str):
        if quote == base:
            raise ConvertionExeption(f'Неудалось перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExeption(f'Неудалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExeption(f'Неудалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f'Неправильно введено число {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/deb9e429e53c193552d668fd/pair/{quote_ticker}/{base_ticker}/{amount}')
        total_base = json.loads(r.content)
        return round(total_base["conversion_result"], 2)