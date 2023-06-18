from .misc import saveable_to_human_readable
from .website_info import SITES_INFO
from typing import Dict, Tuple

PRICEFILES_DIR = r".\prices"

SUPPORTED_WEBSITES = SITES_INFO.keys()
SUPPORTED_BRANDS = ("ADIDAS", "REEBOK", "NEW_BALANCE")
HUMAN_READABLE_BRANDS = tuple([(brand, saveable_to_human_readable(brand)) for brand in SUPPORTED_BRANDS])
SUPPORTED_CURRENCIES = (("EUR", "Euro"),
                        ("GBP", "British pound"),
                        ("CZK", "Czech crown"),
                        ("RUB", "Russian ruble"))
SUPPORTED_QUERIES: Dict[str, Tuple[str]] = {
    "Adidas": ("Gazelle",),
    # "Adidas": ("Gazelle", "Samba", "Forum"),
    # "New Balance": ("2002", "574", "991"),
    # "Reebok": ("Club C", "Classic", "Beatnik")
}
ITEM_COUNT_LIMIT = 20
