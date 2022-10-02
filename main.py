from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep


def search_elements(driver, elem_name, by_id):
    if by_id:
        return driver.find_elements(By.ID, elem_name)
    return driver.find_elements(By.CLASS_NAME, elem_name)


def accept_cookies(driver, cookie_button, by_id, accept_script) -> bool:
    if len(search_elements(driver, cookie_button, by_id)) != 0:
        print("Found cookie button")
        driver.execute_script(accept_script)
        return True

    print("Could not find cookie button")
    return False


def make_search(driver, query: str, search_button: str, button_by_id: bool,
                search_field: str, field_by_id: bool, button_click_script: str) -> bool:
    input_field = search_elements(driver, search_button, button_by_id)

    if len(input_field) != 0:
        print("Trying to search")
        driver.execute_script(button_click_script)
        input_field = search_elements(driver, search_field, field_by_id)
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


def gather_info(driver):
    all_items = driver.find_elements(By.CLASS_NAME, "itemInformation")
    if len(all_items) == 0:
        print("Could not gather info about items")
        return -1

    for i, item in enumerate(all_items):
        name = item.find_elements(By.CLASS_NAME, "itemTitle")[0].find_elements(By.TAG_NAME, "a")[0].text
        if not name:
            print(f"Could not find name of item {i + 1}")

        price = item.find_elements(By.CLASS_NAME, "itemPrice")[0]. \
            find_elements(By.CLASS_NAME, "pri")[0]
        price_with_sale = price.find_elements(By.CLASS_NAME, "now")
        if len(price_with_sale) != 0:
            price = price_with_sale[0]

        if not price:
            print(f"Could not find price of item {i + 1}")

        if name and price:
            print(f"{i + 1} ", name, price.text)

    return 0


def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(executable_path="C:\\progy\\chromedriver.exe", options=chrome_options)
    curr_website = "https://www.footpatrol.com"
    query = "Nike Air Force"
    driver.get(curr_website)

    if not accept_cookies(driver, "accept-all-cookies", False,
                          "document.getElementsByClassName(\"btn btn-level1 accept-all-cookies\")[0]"
                          ".dispatchEvent(new Event(\"click\"))"):
        return -1
    sleep(1)

    if not make_search(driver, query, "searchButton", True, "srchInput", True,
                       "document.getElementById(\"searchButton\")"
                       ".dispatchEvent(new Event(\"click\"))"):
        return -1
    sleep(1)

    sort_items_on_page(driver, ["document.querySelector('[value=price-low-high]').selected = true",
                                "document.getElementById(\"sortFormTop\").dispatchEvent(new Event(\"submit\"))"])
    sleep(1)

    return gather_info(driver)


if __name__ == '__main__':
    main()
