import requests


# https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11

class Connection:
    def get_data(self, url):
        raise NotImplementedError


class Request(Connection):
    def __init__(self, fetch: requests):
        self.fetch = fetch

    def get_data(self, url):
        response = self.fetch.get(url)
        return response.json()


class Request2(Connection):
    def __init__(self, fetch: requests):
        self.fetch = fetch

    def get_data(self, url):
        response = self.fetch.get(url)
        return response.json()


class ApiClient:
    def __init__(self, fetch: Connection):
        self.fetch = fetch

    def get_json(self, url):
        response = self.fetch.get_data(url)
        return response


def pretty_view(data: list[dict]):
    pattern = '|{:^10}|{:^10}|{:^10}|'
    print(pattern.format('currency', 'sale', 'buy'))
    for el in data:
        currency, *_ = el.keys()
        buy = el.get(currency).get('buy')
        sale = el.get(currency).get('sale')
        print(pattern.format(currency, sale, buy))


def adapter_data(data: list[dict]):
    result = [{f"{el.get('ccy')}": {"buy": float(el.get('buy')), "sale": float(el.get('sale'))}} for el in data]
    return result


if __name__ == "__main__":
    client = ApiClient(Request2(requests))
    data = client.get_json(
        "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11"
    )

    pretty_view(adapter_data(data))
