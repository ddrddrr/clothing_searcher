from selenium.webdriver.common.by import By
from price_files_misc import get_price_file_name

# https://answear.cz/c/on and https://answear.cz/c/ona

cookie_button = "//div[@class='flex middle-xs center-xs' and contains(text(),'Souhlasím')]"
search_button = None
search_field = "//input[@id='productsSearch']"

price_sort_scripts = [
    "document.getElementsByClassName(\"BaseSelectDropdown__select__u1BUW"
    " BaseSelectDropdown__selectHasAFilter__wVdDi\")[0].click()",

    "document.getElementsByClassName(\"BaseSelectDropdown__selectList__1vd4p undefined\")[0]"
    ".children[3].click()",

    "document.getElementsByClassName(\"btn col-xs-12 col-lg-12 btn--fluid btn--spaced-bottom btn--sortingSubmit\")[0]"
    ".click()"]


def gather_info(driver) -> bool:
    all_items = driver.find_elements(By.CLASS_NAME, "ProductItem__productCardDescription__2OiTW")
    if len(all_items) == 0:
        print("Could not find any items")
        return False

    price_filename = get_price_file_name(all_items[0].
                                         find_elements(By.CLASS_NAME, "Price__price__3uiSQ")[0].text)
    with open(price_filename, "a", encoding="utf8") as pf:
        print(driver.current_url, file=pf)

        for i, item in enumerate(all_items):
            i = i + 1
            name = item.find_elements(By.CLASS_NAME, "ProductItem__productCardName__RGRRI")
            if len(name) == 0:
                print(f"Could not find name of element {i}")
                continue

            price = item.find_elements(By.CLASS_NAME, "Price__salePrice__tkBzg")
            if len(price) == 0:
                price = item.find_elements(By.CLASS_NAME, "Price__price__3uiSQ")
                if len(price) == 0:
                    print(f"Could not find price for element {i}\n{i} {name[0].text} no price")
                    continue

            print(i, name[0].text, price[0].text, file=pf)

    return True
