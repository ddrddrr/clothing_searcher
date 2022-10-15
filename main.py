import importlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from typing import Optional


# All pages are in form of "https://Optional[www.]NAME.[something]"
def strip_webpage_name(web_adress: str):
    if web_adress.count("www") != 1:
        return web_adress[web_adress.find("//") + 2: web_adress.find(".")]

    dot_index = web_adress.find('.')
    return web_adress[dot_index + 1:
                      dot_index + 1 + web_adress[dot_index + 1:].find('.')]


def search_elements(driver, xpath: str):
    return driver.find_elements(By.XPATH, xpath)  # TODO tests


def accept_cookies(driver, cookie_button: Optional[str]) -> None:
    if cookie_button is None:
        return

    actual_button = search_elements(driver, cookie_button)
    if len(actual_button) != 0:
        print("Found cookie button")
        actual_button[0].click()
        return

    print("Could not find cookie button")


def make_search(driver, query: str, search_button: Optional[str],
                search_field: str) -> bool:
    if search_button is not None:
        input_field = search_elements(driver, search_button)
        if len(input_field) != 0:
            print("Trying to search")
            input_field[0].click()
        else:
            print("Could not find search button")
            return False

    input_field = search_elements(driver, search_field)
    if len(input_field) != 0:
        input_field[0].send_keys(query)
        sleep(0.5)
        input_field[0].send_keys(Keys.ENTER)
    else:
        print("Could not find search_field")
        return False

    return True


def sort_items_on_page(driver, scripts) -> None:
    # TODO think about return value in case of failure
    for script in scripts:
        driver.execute_script(script)


def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(executable_path="C:\\progy\\chromedriver.exe", options=chrome_options)

    pages = ["https://www.footpatrol.com", "https://www.size.co.uk/", "https://www.footlocker.cz"]
    query = "Nike Air Force"

    for page in pages:
        driver.get(page)

        module_name = strip_webpage_name(page)
        curr_site_module = importlib.import_module(module_name)  # TODO think of a better way
        sleep(1)

        accept_cookies(driver, curr_site_module.cookie_button)
        sleep(1)

        if not make_search(driver, query, curr_site_module.search_button, curr_site_module.search_field):
            return -1
        sleep(1)

        sort_items_on_page(driver, curr_site_module.price_sort_scripts)
        sleep(1)

        return curr_site_module.gather_info(driver)


def test_website(site_address):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(executable_path="C:\\progy\\chromedriver.exe", options=chrome_options)
    driver.get(site_address)
    module_name = strip_webpage_name(site_address)
    site_module = importlib.import_module(module_name)

    sleep(2)
    accept_cookies(driver, site_module.cookie_button)
    assert make_search(driver, "New Balance 574", site_module.search_button, site_module.search_field)
    sleep(2)
    sort_items_on_page(driver, site_module.price_sort_scripts)
    sleep(2)
    site_module.gather_info(driver)


if __name__ == '__main__':
    # main()
    test_website("https://answear.cz/c/on")
