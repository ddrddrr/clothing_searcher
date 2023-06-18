import pytest

from ..web_search import accept_cookies
from ..website_info import SITES_INFO
from ..dirver_config import DRIVER
from ..search_config import SUPPORTED_QUERIES
from ..get_items import make_query
from sys import stderr


@pytest.fixture
def website_name():
    return "https://www.hhv.de/shop/en"


def test_website(website_name):
    if DRIVER is None:
        print(f"Driver is not initialized", file=stderr)
        exit(1)

    cookie_info, search_info, sort_scripts, xpath_info = SITES_INFO[website_name]
    DRIVER.get(website_name)
    assert accept_cookies(cookie_info[0], cookie_info[1])

    print(f"Now working on {website_name}")
    seach_is_fine = True
    for brand, models in SUPPORTED_QUERIES.items():
        for model in models:
            query = brand + ' ' + model
            query_res = make_query(query, search_info, sort_scripts, xpath_info)
            if query_res is None:
                seach_is_fine = False
                break

            print(website_name, brand, query_res)

        if not seach_is_fine:
            break

    DRIVER.quit()
