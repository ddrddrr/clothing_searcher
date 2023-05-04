from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from time import sleep
from typing import Optional, List, Tuple
from currency_processing.currency_processing_main import find_currency_in_str, AllCurrencyGroups
import price_output as po
from website_info import COOKIE_INFO, SEARCH_INFO, XPATH_INFO

CHROME_OPTIONS = Options()
CHROME_OPTIONS.add_experimental_option("detach", True)
CHROME_OPTIONS.add_argument("start-maximized")
DRIVER = webdriver.Chrome(executable_path="chromedriver.exe", options=CHROME_OPTIONS)
MAX_SCRIPT_REPEAT = 20


def wait_appear_xpath(xpath: str):
    try:
        found_elem = WebDriverWait(DRIVER, 5). \
            until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))

    except Exception as ex:
        print(ex)
        return None

    return found_elem


def wait_clickable_xpath(xpath: str):
    try:
        found_elem = WebDriverWait(DRIVER, 5). \
            until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))

    except Exception as ex:
        print(ex)
        return None

    return found_elem


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
    cookie_button.click()
    print("Clicked cookie button")
    return True


def make_search(query: str, non_standart_seacrh_scripts: Optional[List[str]],
                search_button_xpath: Optional[str], search_field_xpath: str) -> bool:
    if non_standart_seacrh_scripts is not None:
        if execute_scripts(non_standart_seacrh_scripts):

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
            print("Could not execute search scripts")
            return False

    if search_button_xpath is not None:
        search_button = wait_clickable_xpath(search_button_xpath)
        if search_button is None:
            print("Could not locate search button, skipping")
            return False

        print("Found search button")
        search_button.click()
        print("Clicked search button")

    input_field = wait_appear_xpath(search_field_xpath)
    if input_field is None:
        print("Could not find search_field, skipping")
        return False

    print("Found search field")
    input_field.send_keys(query)
    print("Sent keys")
    sleep(0.5)
    input_field.send_keys(Keys.ENTER)
    print("Entered keys")
    return True


def prep_item_gathering(query: str, cookie_info: COOKIE_INFO, search_info: SEARCH_INFO) -> bool:
    cookie_button_xpath, cookie_scripts = cookie_info
    seacrh_scripts, search_button_xpath, search_field_xpath = search_info
    return (accept_cookies(cookie_button_xpath, cookie_scripts) and
            make_search(query, seacrh_scripts, search_button_xpath, search_field_xpath))


def execute_scripts(scripts: List[str], max_script_repeat=MAX_SCRIPT_REPEAT) -> bool:
    # TODO change this polling to something proper
    i = 0
    same_script_count = 0
    while i < len(scripts):
        script = scripts[i]
        sleep(0.5)
        try:
            DRIVER.execute_script(script)
        except Exception as ex:
            if same_script_count == max_script_repeat:
                return False
            print(f"Problem with script {i}", ex)
            same_script_count += 1
            sleep(0.5)
        else:
            same_script_count = 0
            i += 1
            sleep(0.5)

    return True


def sort_items_on_page(scripts: List[str]) -> bool:
    print("Trying to sort items on page")
    res = execute_scripts(scripts)
    print("Items on page are sorted") if res else print("Could not sort items on page")
    return res


def get_all_items(all_items_xpath):
    all_items = wait_appear_xpath(all_items_xpath)
    if all_items is None:
        print("Could not locate items")
        return None

    all_items = DRIVER.find_elements(By.XPATH, all_items_xpath)
    if len(all_items) == 0:
        print("Could not locate items")
        return None

    return all_items


def get_current_currency(all_items, price_xpath):
    try:
        currency_str = all_items[0].find_elements(By.XPATH, price_xpath)[0].get_attribute("textContent")
    except Exception as ex:
        print(f"{ex}, could not find any price elements")
        return None
    return find_currency_in_str(currency_str)


def get_item_attribute(item, attribute: str, attribute_xpath: str) -> Optional[str]:
    try:
        attribute: Optional[str] = item.find_elements(By.XPATH, attribute_xpath)[0].get_attribute(attribute)
    except Exception as ex:
        print(f"{ex}\nProblem occurred, while trying to find item's {attribute}")
        return None

    if attribute is None:
        print(f"Could not find {attribute} for {attribute_xpath}")

    return attribute


def get_price_name_href(item, name_xpaths: List[str], price_xpath: str, href_xpath: str) \
        -> Tuple[Optional[str], Optional[str], Optional[str]]:
    return (" ".join([get_item_attribute(item, "textContent", name_xpath) for name_xpath in name_xpaths]),
            get_item_attribute(item, "textContent", price_xpath),
            get_item_attribute(item, "href", href_xpath))


def gather_info(xpaths: XPATH_INFO, item_count_limit: int, query: str, currency_groups: AllCurrencyGroups) -> bool:
    lst_query = query.lower().split()
    all_items_xpath, name_xpaths, price_xpath, href_xpath = xpaths
    current_url = DRIVER.current_url

    all_items = get_all_items(all_items_xpath)
    if all_items is None:
        print("Error occured while trying to locate items")
        return False

    currency = get_current_currency(all_items, price_xpath)
    if currency is None:
        print("Error occured while trying to establish currency")
        return False
    current_currency_group = currency_groups.currency_groups[currency]

    price_filename = po.get_price_file_name(currency)
    with open(price_filename, "a", encoding="windows-1252") as price_file:
        price_file.write(f"{current_url}\n")

        item_number = 0
        for i in range(min(item_count_limit, len(all_items))):
            item = all_items[i]

            name, price, href = get_price_name_href(item, name_xpaths, price_xpath, href_xpath)
            if name is None or price is None:
                continue
            if href is None:
                href = current_url

            if po.name_comply_with_query(name, lst_query):
                name, price = po.prep_name_price_for_saving(name, price)
                item_number += 1
                current_currency_group.add_item(price, name, href)
                po.write_one_to_pricefile(item_number, price, name, currency, price_file)
                po.print_one_item(item_number, price, name, currency)

    current_currency_group.save_curr_website_items()
    return True
