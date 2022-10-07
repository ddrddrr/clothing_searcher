from selenium.webdriver.common.by import By

cookie_button = "//*[contains(text(), 'onetrust-accept-btn-handler')]"
search_button = "//input[@id='HeaderSearch_search_query']"
search_field = search_button

cookie_accept_script = "document.getElementById(\"onetrust-accept-btn-handler\")" \
                       ".dispatchEvent(new Event(\"click\"))"
search_button_click_script = "document.getElementsByClassName(\"SearchForm-button\")[0]" \
                             ".dispatchEvent(new Event(\"click\"))"
price_sort_scripts = ["document.getElementById(\"ProductSortBy_selectCustom_sortHelper\").click()",
                      "document.getElementById(\"price-asc\").click()"]


def gather_info(driver) -> bool:
    name_elems = driver.find_elements(By.CLASS_NAME, "ProductName-primary")
    price_elems = driver.find_elements(By.CLASS_NAME, "ProductPrice")
    if len(name_elems) == 0:
        print("Could not gather info about items")
        return False

    for i, name_elem, price_elem in enumerate(zip(name_elems, price_elems)):
        name = name_elem.text
        price_elem_children = price_elem.find_elements(By.CLASS_NAME, "ProductPrice-sale")
        if len(price_elem_children) != 0:
            price = price_elem_children[0].find_elements(By.CLASS_NAME, "ProductPrice-final")[0].text
        else:
            price = price_elem.text

        print(i, name, price)
