from selenium.webdriver.common.by import By

cookie_button = "//button[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']"
search_button = "//input[@id='frm-searchForm-squery']"
search_field = "//input[@id='frm-searchForm-squery']"

price_sort_scripts = [
    "document.getElementById(\"category-filter-order-change\").children[0].removeAttribute(\"selected\")",
    "document.getElementById(\"category-filter-order-change\").children[1].setAttribute(\"selected\",\"\")",
    "document.getElementById(\"category-filter-order-change\").dispatchEvent(new Event(\"change\"))"]


def gather_info(driver) -> bool:
    all_items = driver.find_elements(By.CLASS_NAME, "details")
    if len(all_items) == 0:
        print("Could not find any items")
        return False

    for i, item in enumerate(all_items):
        i = i + 1
        name = item.find_elements(By.XPATH, "//span[@title]")
        if len(name) == 0:
            print(f"Could not find name for element {i}")
            continue

        price = item.find_elements(By.CLASS_NAME, "item-price__new")
        if len(price) == 0:
            price = item.find_elements(By.CLASS_NAME, "price")
            if len(price) == 0:
                print(f"{i} {name[0].text} Could not find price")
                continue

        print(i, name[0].text, price[0].text)

    return True
