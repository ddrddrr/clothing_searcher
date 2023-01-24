from selenium.webdriver.common.by import By
from price_files_misc import get_price_file_name
from typing import Dict, List, Tuple, Optional

SITE_NAME = COOKIE_BUTTON = SEARCH_BUTTON = SEARCH_FIELD \
    = SORT_SCRIPT = ALL_ITEMS_XPATH = PRICE_XPATH = NAME_XPATH = str

SITES_INFO: Dict[SITE_NAME,
                 Tuple[
                     Tuple[Optional[COOKIE_BUTTON], SEARCH_BUTTON, SEARCH_FIELD],
                     List[SORT_SCRIPT],
                     ALL_ITEMS_XPATH,
                     NAME_XPATH,
                     PRICE_XPATH]] = \
    {
        "https://www.footpatrol.com/":
            (("//button[@class='btn btn-level1 accept-all-cookies']",
              "//div[@id='searchButton']",
              "//input[@id='srchInput']"),

             ["document.querySelector('[value=price-low-high]').selected = true",
              "document.getElementById(\"sortFormTop\").dispatchEvent(new Event(\"submit\"))"],

             "//ul[@id='productListMain']/li//span[contains(@class,'itemInformation')]",
             ".//a[@data-e2e='product-listing-name']",
             ".//span[@class='pri' and @data-e2e='product-listing-price'] | "
             ".//span[@class='now']/span[@data-oi-price='']"
             ),

        "https://www.size.co.uk/":
            (("//button[@class='btn btn-level1 accept-all-cookies']",
              "//div[@id='searchButton']",
              "//input[@id='srchInput']"),

             ["document.querySelector('[value=price-low-high]').selected = true",
              "document.getElementById(\"sortFormTop\").dispatchEvent(new Event(\"submit\"))"],

             "//ul[@id='productListMain']/li//span[contains(@class,'itemInformation')]",
             ".//a[@data-e2e='product-listing-name']",
             ".//span[@class='pri' and @data-e2e='product-listing-price'] | "
             ".//span[@class='now']/span[@data-oi-price='']"
             ),

        "https://www.urbanindustry.co.uk/":
            ((None,
              "//input[@id='search-field']",
              "//input[@id='search-field']"),

             [
                 "document.getElementsByClassName(\"snize-main-panel-dropdown-content\")[0]"
                 ".setAttribute(\"style\", \"display: block\")",

                 "document.getElementsByClassName(\"snize-main-panel-dropdown-relevance-desc current\")[0]"
                 ".classList.remove(\'current\')",

                 "document.getElementsByClassName(\"snize-main-panel-dropdown-price-asc\")[0]"
                 ".classList.add(\'current\')",

                 "document.getElementsByClassName(\"snize-main-panel-dropdown-price-asc current\")[0]"
                 ".click()"
             ],

             "//span[@class='snize-overhidden']",
             ".//span[contains(@class,'snize-title')]",
             ".//span[contains(@class,'snize-price')] | .//span[contains(@class,'snize-discounted-price')]"
             )
    }


def gather_info(driver, all_items_xpath, name_xpath, price_xpath) -> bool:
    all_items = driver.find_elements(By.XPATH, all_items_xpath)
    if len(all_items) == 0:
        print("Could not gather info about items")
        return False
    # TODO write in one file, then split
    price_filename = get_price_file_name(
        all_items[0].find_elements(By.XPATH, price_xpath)[0].get_attribute("textContent"))

    with open(price_filename, "a", encoding="utf8") as price_file:
        price_file.write(f"{driver.current_url}\n")

        for i, item in enumerate(all_items):
            i = i + 1
            name = item.find_elements(By.XPATH, name_xpath)[0].get_attribute("textContent")
            if not name:
                print(f"Could not find name of item {i}")
                continue

            price = item.find_elements(By.XPATH, price_xpath)[0].get_attribute("textContent")
            if not price:
                print(f"Could not find price of item {i}")

            if name and price:
                price_file.write(f"{i} {name} {price}\n")
                print(f"{i} ", name, price)

    return True
