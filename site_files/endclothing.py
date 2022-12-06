from selenium.webdriver.common.by import By
from price_files_misc import get_price_file_name

# https://www.endclothing.com/eu

cookie_button = None
search_button = "//*[@class='sc-1ntxmcf-0 eYnDJz']"
search_field = "//*[@class='sc-1oj568y-4 bAuuco']"

price_sort_scripts = ["document.getElementsByClassName('sc-371ia5-3 dTCJWa')[1].click()",
                      "document.getElementsByClassName('sc-371ia5-2 jWLUWk')[0].click()"]


def gather_info(driver) -> bool:
    all_items = driver.find_elements(By.XPATH, "//a[contains(@class,'sc-zofufr-2')]")
    if len(all_items) == 0:
        print("Could not gather info about items")
        return False

    price_filename = get_price_file_name(
        all_items[0].find_elements(
            By.XPATH, ".//span[@data-test='ProductCard__ProductFinalPrice']")[0].text)

    with open(price_filename, "a", encoding="utf8") as pf:
        print(driver.current_url, file=pf)

        for i, item in enumerate(all_items):
            name = item.find_elements(By.XPATH, ".//span[@data-test='ProductCard__PlpName']")
            if not name:
                print(f"Could not find name of item {i + 1}")
                continue

            price = item.find_elements(By.XPATH, ".//span[@data-test='ProductCard__ProductFinalPrice']")
            if not price:
                print(f"Could not find price of item {i + 1}")

            if name and price:
                pf.write(f"{i + 1} {name[0].text} {price[0].text}\n")
                print(f"{i + 1} ", name[0].text, price[0].text)

    return True
