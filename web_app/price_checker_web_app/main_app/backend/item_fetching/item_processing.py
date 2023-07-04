from typing import List, Tuple, Optional
import re
import os
import shutil
import uuid
from ..dirver_config import DRIVER
from .search_config import SCREENSHOT_DIRECTORY, BASE_SCREENSHOT_PATH
from .misc import find_first_digit, find_last_digit

NON_DIGIT_PATTERN = re.compile(r'\D')


class FoundItem:
    __slots__ = ["brand", "name", "price", "currency", "link", "image_path"]

    def __init__(self, name, price, currency, link, image_path):
        self.name = name
        self.price = price
        self.currency = currency
        self.link = link
        self.image_path = image_path

    @staticmethod
    def prep_name_price_for_saving(name: str, price: str) -> Optional[Tuple[str, float]]:
        price = NON_DIGIT_PATTERN.sub('.', price.strip()[find_first_digit(price):find_last_digit(price) + 1])
        try:
            price = float(price)
        except ValueError:
            print("Could not convert price to float")
            return None

        return name.strip().lower(), price

    @staticmethod
    def name_comply_with_query(name: str, query: List[str]) -> bool:
        name = name.lower().split()
        for qword in query:
            for nword in name:
                if qword in nword:
                    return True

        return False

    @staticmethod
    def take_screenshot(item):
        imagepath = os.path.join(SCREENSHOT_DIRECTORY, f"{uuid.uuid4().hex}.png")
        try:
            DRIVER.execute_script("arguments[0].scrollIntoView();", item)
            screenshot = item.screenshot_as_png
        except Exception as ex:
            print(f"Could not take screenshot of {item}\n{ex}")
            return BASE_SCREENSHOT_PATH

        try:
            with open(imagepath, 'wb') as file:
                try:
                    file.write(screenshot)
                except Exception as ex:
                    print(f"Could not save the screenshot of {item}\n{ex}")
                    return BASE_SCREENSHOT_PATH
        except Exception as ex:
            print(f"Could not create file {imagepath}\n{ex}")
            return BASE_SCREENSHOT_PATH

        return imagepath


def clear_screenshot_dir():
    for filename in os.listdir(SCREENSHOT_DIRECTORY):
        file_path = os.path.join(SCREENSHOT_DIRECTORY, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
