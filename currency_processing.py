import requests
from typing import Dict, List
from json import dumps, load
from os import listdir
import currency_proc_misc as cpm
from misc import merge_k_sorted_iterables
from price_output import write_all_to_pricefile, print_all_items


class Currency:
    def __init__(self, name: str, exchange_rates: Dict[str, float]):
        self.name = name
        self.exchange_rates = exchange_rates

    def convert_to_another(self, amount: float, convert_to: str) -> float:
        return amount * self.exchange_rates[convert_to]

    def fill_exchange_rates(self) -> None:
        self.exchange_rates = get_exchange_rates(self.name)


class CurrencyGroup:
    def __init__(self, currency: Currency) -> None:
        self.currency = currency
        self.items: List[cpm.WEBSITE_ITEMS] = []
        self.curr_website_items = []

    def convert_to_all_currencies(self, orig_price: str) -> List[cpm.PRICE]:
        prices = []
        float_price = float(orig_price)
        for convert_to in cpm.CURRENCY_NAMES:
            prices.append(self.currency.convert_to_another(float_price, convert_to))

        return prices

    def add_item(self, price_orig: str, name: str, website_name: str) -> None:
        prices = self.convert_to_all_currencies(price_orig)
        self.curr_website_items.append((prices, name, website_name))

    def save_curr_website_items(self) -> None:
        self.items.append(self.curr_website_items)
        self.curr_website_items = []

    def sort_all_items(self):
        self.items = merge_k_sorted_iterables(self.items)


class AllCurrencyGroups:
    def __init__(self):
        self.currency_groups: Dict[str, CurrencyGroup] = {}
        self.sorted_items = []

    def add_currency_group(self, currency_group: CurrencyGroup):
        self.currency_groups[currency_group.currency.name] = currency_group

    def sort_all_items(self) -> None:
        all_items: List[List[cpm.WEBSITE_ITEMS]] = []
        for _, currency_group in self.currency_groups.items():
            currency_group.sort_all_items()
            all_items.append(currency_group.items)

        self.sorted_items = merge_k_sorted_iterables(all_items)

    def write_all_items_to_file(self, price_file_name: str) -> None:
        if not self.sorted_items:
            self.sort_all_items()

        with open(price_file_name, "w") as pf:
            for i, item in enumerate(self.sorted_items):
                prices, name, website = item
                write_all_to_pricefile(i, prices, name, website, pf)

    def print_items(self):
        if not self.sorted_items:
            self.sort_all_items()

        for i, item in enumerate(self.sorted_items):
            prices, name, website = item
            print_all_items(i, prices, name, website)


# https://currency.getgeoapi.com/documentation/
def get_exchange_rate(currency1: str, currency2: str) -> float:
    key = "130f624c8a310440fb94de898e6ff0ff5ec12acd"
    params = {"api_key": key, "from": currency1, "to": currency2, "format": "json"}
    url = "https://api.getgeoapi.com/v2/currency/convert"
    exchange_info = requests.get(url, params).json()
    return float(exchange_info["rates"][currency2]["rate"])


def get_exchange_rates(base_curr) -> Dict[str, float]:
    exchange_rates = {}
    for curr in cpm.CURRENCY_NAMES:
        exchange_rates[curr] = get_exchange_rate(base_curr, curr)

    return exchange_rates


def store_currencies_info(currencies: cpm.CURRENCIES) -> str:
    filename = cpm.CI_INFO_PATH
    with open(filename, "w") as ci:
        ci_info: Dict[str, Dict[str, float]] = {}
        for currency_name, currency in currencies.items():
            ci_info[currency_name] = currency.exchange_rates
        ci.write(dumps(ci_info, indent=2))

    return filename


def load_currencies_info(ci_filename: str) -> cpm.CURRENCIES:
    currencies: cpm.CURRENCIES = {}
    with open(ci_filename, "r") as ci:
        ci_info: Dict[str, Dict[str, float]] = load(ci)
        for currency_name, exchange_rates in ci_info.items():
            currencies[currency_name] = Currency(currency_name, exchange_rates)

    return currencies


def is_currency_info_up_to_date(dir_with_ci_info_file: str) -> bool:
    entries = listdir(dir_with_ci_info_file)
    for entry in entries:
        if entry in cpm.CI_INFO_PATH:
            return True

    return False


def get_currencies_info(currency_names=cpm.CURRENCY_NAMES) -> Dict[str, Currency]:
    if is_currency_info_up_to_date(cpm.CI_INFO_DIR):
        return load_currencies_info(cpm.CI_INFO_PATH)

    info: cpm.CURRENCIES = {}
    for base_curr in currency_names:
        new_curr = Currency(base_curr, {})
        new_curr.fill_exchange_rates()
        info[base_curr] = new_curr
    store_currencies_info(info)
    return info


def get_all_currency_groups(currency_names=cpm.CURRENCY_NAMES) -> AllCurrencyGroups:
    res = AllCurrencyGroups()
    currencies_info = get_currencies_info(currency_names)
    for currency_name, currency in currencies_info.items():
        res.add_currency_group(CurrencyGroup(currency))

    return res


def find_currency_in_str(string: str) -> str:
    if cpm.EUR_RE.search(string) is not None:
        return "EUR"

    if cpm.POUND_RE.search(string) is not None:
        return "GBP"

    if cpm.CZ_CROWN_RE.search(string) is not None:
        return "CZK"

    return "DEFAULT"
