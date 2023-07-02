from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from typing import Optional, List, Tuple
from .item_processing import FoundItem as fitem
from ..currency_processing.currency_processing_main import find_currency_in_str
from .website_info import COOKIE_INFO, SEARCH_INFO, XPATH_INFO
from ..dirver_config import DRIVER, MAX_SCRIPT_REPEAT
from .search_config import SLEEP_BETWEEN_SCRIPTS
from .waits import (wait_appear_xpath, wait_clickable_xpath,
                    wait_page_refresh_context_manager, wait_page_refresh_decorator)


def accept_cookies(non_standart_button_scripts: Optional[List[str]], cookie_button_xpath: Optional[str]) -> bool:
    if non_standart_button_scripts is not None:
        if execute_scripts(non_standart_button_scripts):
            print("Clicked cookie button")
            if cookie_button_xpath is None:
                return True
        else:
            print("Could not execute cookie scripts, skipping")
            return False

    if cookie_button_xpath is None:
        print("No cookie button on this website")
        return True

    cookie_button = wait_clickable_xpath(cookie_button_xpath)
    if cookie_button is None:
        print("Could not find cookie button, skipping")
        return False

    print("Found cookie button")
    try:
        cookie_button.click()
    except Exception as ex:
        print(f"Could not click {cookie_button_xpath}\n{ex}")
        return False

    print("Clicked cookie button")
    return True


@wait_page_refresh_decorator
def make_search(query: str, non_standard_seacrh_scripts: Optional[List[str]],
                search_button_xpath: Optional[str], search_field_xpath: str) -> bool:
    if non_standard_seacrh_scripts is not None:
        if execute_scripts(non_standard_seacrh_scripts):

            # SPECIAL CASES #################################################################
            if DRIVER.current_url == "https://www.43einhalb.com/#":
                buf = "document.getElementById('search_word').value=" + "'" + query + "'"
                DRIVER.execute_script(buf)
                DRIVER.execute_script("document.getElementById('pageSearchDesktop').submit()")
            #################################################################################

            print("Successfully executed search scripts")
        if search_button_xpath is None and search_field_xpath is None:
            return True
        else:
            print("In case of non-standard search scripts, search has to be made only using them")
            return False

    if search_button_xpath is not None:
        search_button = wait_clickable_xpath(search_button_xpath)
        if search_button is None:
            return False

        print("Found search button")
        try:
            search_button.click()
        except Exception as ex:
            print(f"Could not click button with path {search_button_xpath} ,skipping\n{ex}")
            return False
        print("Clicked search button")

    input_field = wait_appear_xpath(search_field_xpath)
    if input_field is None:
        return False

    print("Found search field")
    try:
        input_field.send_keys(Keys.CONTROL + "a")
        input_field.send_keys(Keys.DELETE)
        input_field.send_keys(query)
        sleep(SLEEP_BETWEEN_SCRIPTS)
        input_field.send_keys(Keys.ENTER)
    except Exception as ex:
        print(f"Could not send keys to search field\n{ex}")
        return False

    print("Sent keys")
    return True


def prep_item_gathering(query: str, cookie_info: COOKIE_INFO, search_info: SEARCH_INFO) -> bool:
    cookie_button_xpath, cookie_scripts = cookie_info
    seacrh_scripts, search_button_xpath, search_field_xpath = search_info
    return (accept_cookies(cookie_button_xpath, cookie_scripts) and
            make_search(query, seacrh_scripts, search_button_xpath, search_field_xpath))


def execute_scripts(scripts: List[str], max_script_repeat=MAX_SCRIPT_REPEAT) -> bool:
    i = 0
    same_script_count = 0
    while i < len(scripts):
        script = scripts[i]
        try:
            with wait_page_refresh_context_manager():
                DRIVER.execute_script(script)
        # TODO differentiate between page-refreshing exceptions and script ones
        except Exception as ex:
            if same_script_count == max_script_repeat:
                print(f"Script {script} have reached the limit of repetition\n{ex}")
                return False
            same_script_count += 1
        else:
            same_script_count = 0
            i += 1
        finally:
            sleep(SLEEP_BETWEEN_SCRIPTS)

    return True


def sort_items_on_page(scripts: List[str]) -> bool:
    print("Trying to sort items on page")
    res = execute_scripts(scripts)
    print("Items on page are sorted") if res else print("Could not sort items on page")
    return res


def get_all_items(all_items_xpath):
    single_item = wait_appear_xpath(all_items_xpath)
    if single_item is not None:
        all_items = DRIVER.find_elements(By.XPATH, all_items_xpath)
        return all_items if all_items else None

    return None


def get_current_currency(all_items, price_xpath):
    try:
        currency_str = all_items[0].find_elements(By.XPATH, price_xpath)[0].get_attribute("textContent")
    except Exception as ex:
        print(f"{ex}, could not find any price elements")
        return None
    return find_currency_in_str(currency_str)


def get_item_attribute(item, attribute: str, attribute_xpath: str) -> Optional[str]:
    try:
        element = item.find_elements(By.XPATH, attribute_xpath)
        if element:
            attribute: Optional[str] = element[0].get_attribute(attribute)
    except Exception as ex:
        print(f"Problem occurred, while trying to find item's {attribute} by {attribute_xpath}\n{ex}")
        return ""

    if attribute is None:
        print(f"Could not find {attribute} for {attribute_xpath}")
        return ""

    return attribute


def get_price_name_href(item, name_xpaths: List[str], price_xpath: str, href_xpath: str) \
        -> Tuple[Optional[str], Optional[str], Optional[str]]:
    return (" ".join([get_item_attribute(item, "textContent", name_xpath) for name_xpath in name_xpaths]),
            get_item_attribute(item, "textContent", price_xpath),
            get_item_attribute(item, "href", href_xpath))


def retrieve_website_items(item_limit: int, all_items,
                           name_xpaths: List[str], price_xpath: str, href_xpath: str,
                           current_url: str, query_words: List[str],
                           currency: str) -> Optional[List[fitem]]:
    items = []
    for i, item in enumerate(all_items, item_limit):

        name, price, href = get_price_name_href(item, name_xpaths, price_xpath, href_xpath)
        if name is None or price is None:
            continue

        if href is None:
            href = current_url

        if fitem.name_comply_with_query(name, query_words):
            res = fitem.prep_name_price_for_saving(name, price)
            if res is None:
                return None
            name, price = res
            new_item = fitem(name, price, currency, href)
            items.append(new_item)

    return items


def get_currency_and_item_info(xpaths: XPATH_INFO, item_count_limit: int, query: str) \
        -> Optional[List[fitem]]:
    # TODO it will be prepared in to_python() of the django form in future
    lst_query = query.lower().split()
    all_items_xpath, name_xpaths, price_xpath, href_xpath = xpaths
    current_url = DRIVER.current_url

    all_items = get_all_items(all_items_xpath)
    if all_items is None:
        print(f"Error occured while trying to locate items, using {all_items_xpath}")
        return None

    currency = get_current_currency(all_items, price_xpath)
    if currency is None:
        print(f"Error occured while trying to establish currency, using {price_xpath}")
        return None

    items = retrieve_website_items(min(item_count_limit, len(all_items)),
                                   all_items,
                                   name_xpaths, price_xpath, href_xpath,
                                   current_url, lst_query,
                                   currency)
    if items:
        return items

    return None
