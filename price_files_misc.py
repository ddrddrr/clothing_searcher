import re
import os


def pricefile_name_gen():
    for name in ["prices\\prices_euro", "prices\\prices_pounds",
                 "prices\\prices_cz", "prices\\prices_default"]:
        yield name


def create_price_files() -> None:
    for name in pricefile_name_gen():
        f = open(name, "w")
        f.close()


def destroy_price_files() -> None:
    for name in pricefile_name_gen():
        os.remove(name)


def get_price_file_name(price: str) -> str:
    if re.search(r"(€+|[Ee]uro)", price):
        return "prices\\prices_euro"

    if re.search(r"(£+|[Pp]ound)", price):
        return "prices\\prices_pounds"

    if re.search(r"([Kk][Čč])+", price):
        return "prices\\prices_cz"

    return "prices\\prices_default"


def sort_price_files():
    pass


def combine_price_files():
    pass
