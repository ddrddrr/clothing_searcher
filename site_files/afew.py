from selenium.webdriver.common.by import By
from price_files_misc import get_price_file_name

# https://en.afew-store.com/

cookie_button = "//button[@id='onetrust-reject-all-handler']"
search_button = "//input[@name='q' and @type='search']"
search_field = "//input[@name='q' and @type='search']"

price_sort_scripts = ["document.getElementsByClassName(\"findify-components--button btn collapsed\")[0].click()",
                      "document.getElementsByClassName(\"findify-components--button btn nav-link\").item(2).click()"]


def gather_info(driver) -> bool:
    all_items = driver.find_elements(By.CLASS_NAME, "product-row")[0].find_elements(By.CLASS_NAME, "col")
    if len(all_items) == 0:
        print("Could not find any items")
        return False

    price_filename = get_price_file_name(all_items[0].find_elements
                                         (By.CLASS_NAME, "price")[0].get_attribute("textContent"))
    with open(price_filename, "a", encoding="utf8") as pf:
        print(driver.current_url, file=pf)

        for i, item in enumerate(all_items):
            name = item.find_elements(By.CLASS_NAME, "card-title")
            if len(name) == 0:
                print(f"Could not find name for element {i + 1}")
                continue
            price = item.find_elements(By.CLASS_NAME, "price")
            if len(price) == 0:
                print(f"{i + 1} {name[0].text} Price not found")
                continue

            print(i + 1, name[0].get_attribute("textContent"), price[0].get_attribute("textContent"), file=pf)

    return True
