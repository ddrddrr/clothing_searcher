from typing import Dict, List, Tuple
import re
from datetime import date

CURRENCY_NAMES = ("EUR", "GBP", "CZK", "RUB")
# ??
CURRENCY_NAME = str
CURRENCIES = Dict[CURRENCY_NAME, 'Currency']
CI_INFO = Dict[CURRENCY_NAME, Dict[CURRENCY_NAME, float]]
CI_INFO_DIR = r".\prices"
CI_INFO_PATH_TEMPLATE = rf"{CI_INFO_DIR}\currencies_info_"
CI_INFO_PATH = f"{CI_INFO_PATH_TEMPLATE}{date.today()}.json"

# We are checking multiple objects in a loop, so
# it is more efficient to compile REs in advance
EUR_RE = re.compile(r"(€|eur)", re.IGNORECASE)
POUND_RE = re.compile(r"(£|pound|gbp)", re.IGNORECASE)
CZ_CROWN_RE = re.compile(r"kč|czk|czech crown", re.IGNORECASE)

WEBSITE_NAME = ITEM_NAME = str
PRICE = float
WEBSITE_ITEM = Tuple[List[PRICE], ITEM_NAME, WEBSITE_NAME]
WEBSITE_ITEMS = List[WEBSITE_ITEM]
