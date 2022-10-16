import importlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from typing import Optional


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

    with open("website_names", "r") as website_names, open("module_names", "r") as module_names:
        query = "Nike Air Force"
        for website_name, module_name in map(
                lambda names: (names[0][:names[0].find(";")], names[1][:names[1].find(";")]),
                zip(website_names, module_names)):
            try:
                driver.get(website_name)
            except Exception as ex:
                print(f"{ex}\nCould not open {website_name}, skipping")
                continue

            try:
                curr_site_module = importlib.import_module(module_name)  # TODO think of a better way
            except Exception as ex:
                print(f"{ex}\nCould not import module {module_name}, skipping")
                continue
            sleep(3)

            try:
                accept_cookies(driver, curr_site_module.cookie_button)
            except Exception as ex:
                print(f"{ex}\nAn error occured during trying to accept cookies on {website_name}, skipping")
                continue
            sleep(3)

            try:
                make_search(driver, query, curr_site_module.search_button, curr_site_module.search_field)
            except Exception as ex:
                print(f"{ex}\nAn error occured during the search fase on {website_name}, skipping")
                continue

            sleep(3)

            try:
                sort_items_on_page(driver, curr_site_module.price_sort_scripts)
            except Exception as ex:
                print(f"{ex}\nAn error occured during the sorting phase on {website_name}, skipping")
                continue
            sleep(3)

            print(f"{website_name}:")
            try:
                if not curr_site_module.gather_info(driver):
                    print(f"Could not gather info on {website_name}")
            except Exception as ex:
                print(f"{ex}\nAn error occured during the \"gather info\" phase, skipping {website_name}")
                continue

            for i in range(100):
                print('=', end='')
            print()


def test_website(site_address):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(executable_path="C:\\progy\\chromedriver.exe", options=chrome_options)
    driver.get(site_address)
    # module_name = get_module_name(site_address)
    site_module = importlib.import_module("afew")

    sleep(2)
    accept_cookies(driver, site_module.cookie_button)
    assert make_search(driver, "New Balance 574", site_module.search_button, site_module.search_field)
    sleep(2)
    sort_items_on_page(driver, site_module.price_sort_scripts)
    sleep(2)
    site_module.gather_info(driver)


if __name__ == '__main__':
    #main()
    test_website("https://en.afew-store.com/")
