import importlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from typing import Optional, List, Tuple
import on_site_search
from price_files_misc import create_price_files


def accept_cookies(driver, cookie_button: Optional[str]) -> None:
    assert driver is not None

    if cookie_button is None:
        return

    actual_button = driver.find_elements(By.XPATH, cookie_button)
    if actual_button is not None:
        print("Found cookie button")
        actual_button[0].click()
        return

    print("Could not find cookie button")


# TODO put selenium functions in try-catch blocks
#  in order to avoid crashing the program, whenever there is a problem
def make_search(driver, query: str, search_button: Optional[str],
                search_field: str) -> bool:
    assert driver is not None

    if search_button is not None:
        button = driver.find_elements(By.XPATH, search_button)
        if button is not None:
            print("Trying to search")
            button[0].click()
        else:
            print("Could not find search button")
            return False

    input_field = driver.find_elements(By.XPATH, search_field)
    if input_field is not None:
        input_field[0].send_keys(query)
        sleep(0.5)
        input_field[0].send_keys(Keys.ENTER)
    else:
        print("Could not find search_field")
        return False

    return True


def prep_item_gathering(driver, query: str, buttons: Tuple[Optional[str], Optional[str], str]) -> None:
    cookie_button, search_button, search_field = buttons
    try:
        accept_cookies(driver, cookie_button)
    except Exception as ex:
        print(f"{ex}Problem during cookie acception")
    sleep(1)
    assert make_search(driver, query, search_button, search_field)


def sort_items_on_page(driver, scripts: List[str]) -> None:
    # TODO think about return value in case of failure and how to check for failures
    assert driver is not None

    for script in scripts:
        driver.execute_script(script)
        sleep(0.5)


# TODO replace some of the sleep() funs with proper selenium waits
def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(executable_path="C:\\progy\\chromedriver.exe", options=chrome_options)

    with open("names_and_modules\\website_names", "r") as website_names, \
            open("names_and_modules\\module_names", "r") as module_names:
        query = "Nike Air Force"
        create_price_files()

        for website_name, module_name in map(
                lambda names: (names[0][:names[0].find(";")], names[1][:names[1].find(";")]),
                zip(website_names, module_names)):
            try:
                driver.get(website_name)
            except Exception as ex:
                print(f"{ex}\nCould not open {website_name}, skipping")
                continue

            try:
                curr_site_module = importlib.import_module("site_files." + module_name)
            except Exception as ex:
                print(f"{ex}\nCould not import module {module_name}, skipping")
                continue
            sleep(3)

            try:
                accept_cookies(driver, curr_site_module.cookie_button)
            except Exception as ex:
                print(f"{ex}\nAn error occurred during trying to accept cookies on {website_name}, skipping")
                continue
            sleep(3)

            try:
                make_search(driver, query, curr_site_module.search_button, curr_site_module.search_field)
            except Exception as ex:
                print(f"{ex}\nAn error occurred during the search phase on {website_name}, skipping")
                continue

            sleep(3)

            try:
                sort_items_on_page(driver, curr_site_module.price_sort_scripts)
            except Exception as ex:
                print(f"{ex}\nAn error occurred during the sorting phase on {website_name}, skipping")
                continue
            sleep(3)

            print(f"{website_name}:")
            try:
                if not curr_site_module.gather_info(driver):
                    print(f"Could not gather info on {website_name}")
            except Exception as ex:
                print(f"{ex}\nAn error occurred during the \"gather info\" phase, skipping {website_name}")
                continue

            for i in range(100):
                print('=', end='')
            print()


def remove_last_dot(name: str):
    new = name[name.find(".") + 1:]
    return new[:new.find(".")]


def take_screenshots():
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(executable_path="C:\\progy\\chromedriver.exe", options=chrome_options)
    with open("sneaker_wpages.txt") as wpages:
        for name in wpages:
            try:
                driver.get(name)
            except Exception as ex:
                continue

            sleep(0.5)
            try:
                driver.get_screenshot_as_file(f".\\screenshots\\{remove_last_dot(name)}.png")
            except Exception as ex:
                continue


def test_website(website_name):
    buttons, sort_scripts, \
    all_items_xpath, name_xpath, price_xpath = on_site_search.SITES_INFO[website_name]

    query = "New balance 574"

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(executable_path="../chromedriver.exe", options=chrome_options)

    driver.get(website_name)
    create_price_files()

    sleep(1)
    prep_item_gathering(driver, query, buttons)
    sleep(1)
    sort_items_on_page(driver, sort_scripts)
    sleep(1)
    on_site_search.gather_info(driver, all_items_xpath, name_xpath, price_xpath)


if __name__ == '__main__':
    # main()
    test_website("https://www.urbanindustry.co.uk/")
    # take_screenshots()
