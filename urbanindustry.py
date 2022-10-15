from selenium.webdriver.common.by import By

# https://www.urbanindustry.co.uk/

cookie_button = None
search_button = "//input[@id='search-field']"
search_field = "//input[@id='search-field']"

price_sort_scripts = [
    "document.getElementsByClassName(\"snize-main-panel-dropdown-content\")[0]"
    ".setAttribute(\"style\", \"display: block\")",

    "document.getElementsByClassName(\"snize-main-panel-dropdown-relevance-desc current\")[0]"
    ".classList.remove(\'current\')",

    "document.getElementsByClassName(\"snize-main-panel-dropdown-price-asc\")[0]"
    ".classList.add(\'current\')",

    "document.getElementsByClassName(\"snize-main-panel-dropdown-price-asc current\")[0]"
    ".click()"]


def gather_info(driver) -> bool:
    all_items = driver.find_elements(By.CLASS_NAME, "snize-overhidden")
    if len(all_items) == 0:
        print("Could not find any items")
        return False

    for i, item in enumerate(all_items):
        i = i + 1
        name = item.find_elements(By.CLASS_NAME, "snize-title")
        if len(name) == 0:
            print(f"Could not find name for element {i}")
            continue

        price = item.find_elements(By.CLASS_NAME, "snize-price-with-discount")
        if len(price) == 0:
            price = item.find_elements(By.CLASS_NAME, "snize-price")
            if len(price) == 0:
                print(f"Could not find price for element {i}\n{i} {name[0].text} no price")
                continue

        print(i, name[0].text, price[0].text)

    return True
