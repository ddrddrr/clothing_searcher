from typing import List, Tuple, Optional
from .misc import find_first_digit, find_last_digit
import re

NON_DIGIT_PATTERN = re.compile(r'\D')


class FoundItem:
    __slots__ = ["brand", "name", "price", "currency", "link"]

    def __init__(self, name, price, currency, link):
        self.name = name
        self.price = price
        self.currency = currency
        self.link = link

    @staticmethod
    def prep_name_price_for_saving(name: str, price: str) -> Optional[Tuple[str, float]]:
        price = NON_DIGIT_PATTERN.sub('.', price.strip()[find_first_digit(price):find_last_digit(price) + 1])
        try:
            price = float(price)
        except ValueError:
            print("Could not convert price to float")
            return None

        return name.strip().lower(), price

    @staticmethod
    def name_comply_with_query(name: str, query: List[str]) -> bool:
        name = name.lower().split()
        for qword in query:
            for nword in name:
                if qword in nword:
                    return True

        return False
