import pytest

from web_app.price_checker_web_app.main_app.backend.item_fetching.web_search import accept_cookies
from web_app.price_checker_web_app.main_app.backend.item_fetching.website_info import SITES_INFO
from ..dirver_config import DRIVER
from web_app.price_checker_web_app.main_app.backend.item_fetching.search_config import SUPPORTED_QUERIES
from web_app.price_checker_web_app.main_app.backend.item_fetching.get_items import make_query


@pytest.fixture
def website_name():
    return "https://www.hhv.de/shop/en"


def test_website(website_name):
    if DRIVER is None:
        print(f"Driver is not initialized")
        exit(1)

    cookie_info, search_info, sort_scripts, xpath_info = SITES_INFO[website_name]
    DRIVER.get(website_name)
    assert accept_cookies(cookie_info[0], cookie_info[1])

    print(f"Now working on {website_name}")
    for brand, models in SUPPORTED_QUERIES.items():
        for model in models:
            query = brand + ' ' + model
            query_res = make_query(query, search_info, sort_scripts, xpath_info)
            if query_res is None:
                assert False
            print(website_name, brand, query)
            for item in query_res:
                #print(item)
                try:
                    print(f"{item.name} -- {item.price} -- {item.link}")
                except Exception as _:
                    pass

    DRIVER.quit()
