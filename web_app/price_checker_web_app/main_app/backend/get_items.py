from time import sleep
from typing import Tuple, List, Optional
from .web_search import make_search, sort_items_on_page, get_currency_and_item_info, accept_cookies, NAME, PRICE, HREF
from .website_info import SITES_INFO, SEARCH_INFO, SORT_SCRIPT, XPATH_INFO
from .misc import strip_website_name
from .dirver_config import DRIVER
from .search_config import ITEM_COUNT_LIMIT, SUPPORTED_QUERIES
from sys import stderr


def make_query(query: str, search_info: SEARCH_INFO,
               sort_scripts: List[SORT_SCRIPT], xpath_info: XPATH_INFO) \
        -> Optional[Tuple[str, List[Tuple[NAME, PRICE, HREF]]]]:
    if not make_search(query, search_info[0], search_info[1], search_info[2]):
        print(f"Could not make a search on query {query}, skipping", file=stderr)
        return None

    if not sort_items_on_page(sort_scripts):
        print("Could not execute one of sorting scripts, skipping", file=stderr)
        return None

    # TODO change that to something proper
    sleep(2)

    currency_and_items = get_currency_and_item_info(xpath_info, ITEM_COUNT_LIMIT, query)
    if currency_and_items is None:
        print("Could not gather info about items, skipping", file=stderr)
        return None
    print("Got currency and items")
    return currency_and_items


def get_item_info() -> Tuple[str, str, Tuple[str, List[Tuple[NAME, PRICE, HREF]]]]:
    if DRIVER is None:
        print(f"Driver is not initialized", file=stderr)
        exit(1)

    for website_name, (cookie_info, search_info, sort_scripts, xpath_info) in SITES_INFO.items():
        try:
            DRIVER.get(website_name)
        except Exception as ex:
            print(f"{ex}\nCould not open {website_name}, skipping", file=stderr)
            continue

        if not accept_cookies(cookie_info[0], cookie_info[1]):
            print(f"Could not accept cookies on {website_name}, skipping", file=stderr)
            continue

        print(f"Now working on {website_name}")
        seach_is_fine = True
        for brand, models in SUPPORTED_QUERIES.items():
            for model in models:
                query = brand + ' ' + model
                query_res = make_query(query, search_info, sort_scripts, xpath_info)
                if query_res is None:
                    seach_is_fine = False
                    break

                yield website_name, brand, query_res

            if not seach_is_fine:
                break

    DRIVER.quit()


def take_screenshots():
    with open(r"C:\Users\nenuz\Desktop\sneaker_wpages.txt") as wpages:
        for name in wpages:
            try:
                DRIVER.get(name)
            except Exception as ex:
                print(f"{name}\n{ex}")
                continue

            screenshot_path = f".\\screenshots\\{strip_website_name(name)}.png"
            sleep(3)
            try:
                DRIVER.save_screenshot(screenshot_path)
            except Exception as ex:
                print(f"{name}\n{ex}")

