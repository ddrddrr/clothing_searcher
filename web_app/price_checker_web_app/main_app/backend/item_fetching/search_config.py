from ..item_fetching.misc import saveable_to_human_readable
from ..item_fetching.website_info import SITES_INFO
from typing import Dict, List

PRICEFILES_DIR = r".\prices"

SUPPORTED_WEBSITES = SITES_INFO.keys()
SUPPORTED_BRANDS = ("ADIDAS", "REEBOK", "NEW_BALANCE")
HUMAN_READABLE_BRANDS = tuple([(brand, saveable_to_human_readable(brand)) for brand in SUPPORTED_BRANDS])
SUPPORTED_CURRENCIES = (("EUR", "Euro"),
                        ("GBP", "British pound"),
                        ("CZK", "Czech crown"),
                        ("RUB", "Russian ruble"))
SUPPORTED_QUERIES: Dict[str, List[str]] = {
    "Adidas": ["Gazelle", "Samba", "Forum"],
    # "New Balance": ["2002", "574", "991"],
    # "Reebok": ["Club C", "Classic", "Beatnik"]
}
# all in seconds
ITEM_COUNT_LIMIT = 20
SLEEP_FOR_WAITS = 3
SLEEP_BETWEEN_SCRIPTS = 0.2
SLEEP_PAGE_REFRESH = 3
