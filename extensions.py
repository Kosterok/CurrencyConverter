import requests
import json

class APIException(Exception):
    pass

class CurrencyConverter:
    currencies = {
        'биткоин': 'BTC',
        'этериум': 'ETH',
        'хрп': 'XRP',
        'солана': 'SOL',
        'бинанс': 'BNB',
        'додж': 'DOGE',
        'биткоин': 'BTC',
        'доллар': 'USD',
        'евро': 'EUR',
        'рубль': 'RUB'
    }

    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        base = base.lower()
        quote = quote.lower()

        if base == quote:
            raise APIException("Невозможно перевести одинаковые валюты.")

        if base not in CurrencyConverter.currencies:
            raise APIException(f"Неизвестная валюта: {base}")

        if quote not in CurrencyConverter.currencies:
            raise APIException(f"Неизвестная валюта: {quote}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество: {amount}")

        url = f"https://min-api.cryptocompare.com/data/price?fsym={CurrencyConverter.currencies[base]}&tsyms={CurrencyConverter.currencies[quote]}"
        response = requests.get(url)

        if response.status_code != 200:
            raise APIException("Ошибка при запросе к API валют.")

        try:
            data = json.loads(response.content)
            rate = data[CurrencyConverter.currencies[quote]]
        except Exception:
            raise APIException("Ошибка обработки ответа от API.")

        return rate * amount
