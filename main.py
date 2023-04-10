from time import sleep
import web_search as ws
from website_info import SITES_INFO
from currency_processing import get_all_currency_groups
from price_output import PRICEFILES_DIR

SORTED_ITEMS_PATH = rf"{PRICEFILES_DIR}\sorted_items.txt"


def print_splitting_line():
    for i in range(100):
        print("--", end='')
    print()
    print()


def strip_website_name(name: str) -> str:
    first_dot = 0
    last_dot = 0
    for i, char in enumerate(name):
        if char == '.':
            if first_dot == 0:
                first_dot = i
            else:
                last_dot = i
                break

    return name[first_dot + 1:last_dot]


def main():
    try:
        assert ws.DRIVER is not None
    except Exception as ex:
        print(f"{ex}\nx, driver is not initialized, try restarting the program")
        exit(1)
    # PARAMS -----------------------
    item_count_limit = 10  # to look up on each website
    query = 'New Balance 574'
    # ------------------------------

    # create_price_files()
    currency_groups = get_all_currency_groups()
    for website_name, (cookie_info, search_info, sort_scripts, xpath_info) in SITES_INFO.items():
        try:
            ws.DRIVER.get(website_name)
        except Exception as ex:
            print(f"{ex}\nCould not open {website_name}, skipping")
            print_splitting_line()
            continue

        print(f"Now working on {website_name}")

        if not ws.prep_item_gathering(query, cookie_info, search_info):
            print("Could not make a search, skipping")
            print_splitting_line()
            continue

        if not ws.sort_items_on_page(sort_scripts):
            print("Could not execute one of sorting scripts, skipping")
            print_splitting_line()
            continue
        sleep(2)

        if not ws.gather_info(xpath_info, item_count_limit, query, currency_groups):
            print("Could not gather info about items, skipping")

        print_splitting_line()

    currency_groups.write_all_items_to_file(SORTED_ITEMS_PATH)
    # driver.quit()


def remove_last_dot(name: str):
    new = name[name.find(".") + 1:]
    return new[:new.find(".")]


def take_screenshots():
    with open(r"C:\Users\nenuz\Desktop\sneaker_wpages.txt") as wpages:
        for name in wpages:
            try:
                ws.DRIVER.get(name)
            except Exception as ex:
                print(f"{name}\n{ex}")
                continue

            screenshot_path = f".\\screenshots\\{strip_website_name(name)}.png"
            sleep(3)
            try:
                ws.DRIVER.save_screenshot(screenshot_path)
            except Exception as ex:
                print(f"{name}\n{ex}")


def test_website(website_name):
    cookie_info, search_info, sort_scripts, xpath_info = SITES_INFO[website_name]

    # PARAMS -----------------------
    item_count_limit = 10  # to look up on each website
    query = "New Balance 574"
    # ------------------------------

    currency_groups = get_all_currency_groups()
    try:
        ws.DRIVER.get(website_name)
    except Exception as ex:
        print(f"{ex}\nCould not open {website_name}, skipping")
        return

    print(f"Now working on {website_name}")

    if not ws.prep_item_gathering(query, cookie_info, search_info):
        print("Could not make a search, skipping")
        return

    if not ws.sort_items_on_page(sort_scripts):
        print("Could not execute one of sorting scripts, skipping")
        return
    sleep(2)

    if not ws.gather_info(xpath_info, item_count_limit, query, currency_groups):
        print("Could not gather info about items, skipping")

    print()
    print()
    currency_groups.write_all_items_to_file(SORTED_ITEMS_PATH)
    currency_groups.print_items()


if __name__ == '__main__':
    #main()
    test_website("https://www.hhv.de/shop/en")
    #take_screenshots()
    # combine_price_files()
    # get_exchange_rate("EUR", "RUB")
