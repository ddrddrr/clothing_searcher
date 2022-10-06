import importlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep


# All pages are in form of "https://www.NAME.domain"
def strip_webpage_name(web_adress: str):
    return web_adress[web_adress.find(".") + 1: web_adress.rfind(".")]


def search_elements(driver, elem_name, by_id):
    if by_id:
        return driver.find_elements(By.ID, elem_name)
    return driver.find_elements(By.XPATH, f"//*[@class='{elem_name}']")  # TODO tests


def accept_cookies(driver, cookie_button: tuple[str, bool], accept_script) -> bool:
    if cookie_button is None:
        return True

    button = cookie_button[0]
    by_id = cookie_button[1]
    actual_button = search_elements(driver, button, by_id)
    if len(actual_button) != 0:
        print("Found cookie button")
        actual_button[0].click()
        # driver.execute_script(accept_script)
        return True

    print("Could not find cookie button")
    return False


def make_search(driver, query: str, search_button: tuple[str, bool],
                search_field: tuple[str, bool], button_click_script: str) -> bool:
    input_field = search_elements(driver, search_button[0], search_button[1])
    if len(input_field) != 0:
        print("Trying to search")
        # driver.execute_script(button_click_script)
        input_field[0].click()
        input_field = search_elements(driver, search_field[0], search_field[1])
        if len(input_field) != 0:
            input_field[0].send_keys(query)
            input_field[0].send_keys(Keys.ENTER)
        else:
            print("Could not find search_field")
            return False
    else:
        print("Could not find search button")
        return False

    return True


def sort_items_on_page(driver, scripts):
    # TODO think about return value in case of failure
    for script in scripts:
        driver.execute_script(script)


def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(executable_path="C:\\progy\\chromedriver.exe", options=chrome_options)

    pages = ["https://www.footlocker.cz", "https://www.footpatrol.com"]
    query = "Nike Air Force"

    for page in pages:
        driver.get(page)

        module_name = strip_webpage_name(page)
        curr_site_module = importlib.import_module(module_name) #TODO think of a better way
        sleep(1)

        if not accept_cookies(driver, curr_site_module.cookie_button, curr_site_module.cookie_accept_script):
            return -1
        sleep(1)

        if not make_search(driver, query, curr_site_module.search_button, curr_site_module.search_field,
                           curr_site_module.search_button_click_script):
            return -1
        sleep(1)

        sort_items_on_page(driver, curr_site_module.price_sort_scripts)
        sleep(1)

        return curr_site_module.gather_info(driver)


def test_footlocker():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(executable_path="C:\\progy\\chromedriver.exe", options=chrome_options)
    driver.get("https://www.footlocker.cz")
    sleep(4)
    make_search(driver, "New Balance 574", ("HeaderSearch_search_query", True), ("HeaderSearch_search_query", True),
                "document.getElementsByClassName(\"SearchForm-button\")[0]"
                ".dispatchEvent(new Event(\"click\"))")


if __name__ == '__main__':
    # main()
    test_footlocker()
