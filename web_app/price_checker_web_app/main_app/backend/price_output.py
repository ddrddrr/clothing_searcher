import os
from typing import List, TextIO, Union, Tuple, Optional
from .currency_processing.currency_proc_config import CURRENCY_NAMES
from .misc import find_first_digit, find_last_digit
from .search_config import PRICEFILES_DIR
import re

NON_DIGIT_PATTERN = re.compile(r'\D')


def prep_name_price_for_saving(name: str, price: str) -> Optional[Tuple[str, float]]:
    price = NON_DIGIT_PATTERN.sub('.', price.strip()[find_first_digit(price):find_last_digit(price) + 1])
    try:
        price = float(price)
    except ValueError:
        return None

    return name.strip(), price


# def format_price(price: Union[str, float]) -> str:
#     if isinstance(price, float):
#         price = str(price)
#     if len(price) > 10:
#         price = price[:10]
#
#     return price
#
#
# def write_one_to_pricefile(number: int, price: str, name: str, currency_name: str, price_file: TextIO):
#     price = format_price(price)
#     price_file.write(f"{number:<3} | {name.strip():<70} | {price:<10} {currency_name}")
#
#
# def write_all_to_pricefile(number: int, prices: List[Union[str, float]],
#                            name: str, website_name: str, price_file: TextIO):
#     price_file.write(f"{number:<3} | {name.strip():<70} ")
#     for price, currency_name in zip(prices, CURRENCY_NAMES):
#         price = format_price(price)
#         price_file.write(f" | {price:<10} {currency_name}")
#
#     price_file.write(f" | {website_name}\n")
#
#
# def print_one_item(number: int, price: str, name: str, currency_name: str):
#     price = format_price(price)
#     print(f"{number:<3} | {name.strip():<70} | {price:<10} {currency_name}")
#
#
# def print_all_items(number: int, prices: List[Union[str, float]],
#                     name: str, website_name: str):
#     print(f"{number:<3} | {name.strip():<70} ", end="")
#     for price, currency_name in zip(prices, CURRENCY_NAMES):
#         price = format_price(price)
#         print(f" | {price:<10} {currency_name}", end="")
#
#     print(f" | {website_name}")
#
#
# def get_price_file_name(currency: str) -> str:
#     return rf"{PRICEFILES_DIR}\prices_{currency}.txt"
#
#
# def pricefile_name_gen():
#     for currency in CURRENCY_NAMES:
#         yield get_price_file_name(currency)
#
#
# def destroy_price_files() -> None:
#     for name in pricefile_name_gen():
#         os.remove(name)


def name_comply_with_query(name: str, query: List[str]) -> bool:
    name = name.lower().split()
    for qword in query:
        for nword in name:
            if qword in nword:
                return True

    return False
