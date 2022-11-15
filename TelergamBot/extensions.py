import requests
import json

from config import API_KEY, keys
# --------------------------------


# Класс исключения
class APIException(Exception):
    pass
# --------------------------------


# Класс конвертирования валюты
class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> float:
        if base == quote:
            raise APIException(f'Введены одинаковые валюты: {base}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}')

        # создаем строку из пары тикеров для отправки запроса
        pairs = base_ticker + quote_ticker
        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={pairs}&key={API_KEY}')
        # получаем курс валют 1 к 1
        curs = json.loads(r.content)['data'][pairs]
        # и возвращаем общее количество
        return round((float(curs) * amount), 2)
