from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait, TimeoutException
from selenium.webdriver.support import expected_conditions
from contextlib import contextmanager
from .search_config import SLEEP_FOR_WAITS, SLEEP_PAGE_REFRESH
from ..dirver_config import DRIVER


# plain decorator
# in case of non-javascript(probably AJAX) actions made from driver function just waits for SLEEP_PAGE_REFRESH seconds
def wait_page_refresh_decorator(func):
    def execute_func_and_wait(*args, **kwargs):
        try:
            WebDriverWait(DRIVER, SLEEP_FOR_WAITS).until(
                    expected_conditions.presence_of_element_located((By.TAG_NAME, 'html')))
            old_page = DRIVER.find_element(By.TAG_NAME, 'html')
        except NoSuchElementException as ex:
            print(f"Can't locate the 'html' tag\n{ex}")
            return None
        except Exception as ex:
            print(f"Could not execute {func}\n{ex}")
            return None

        try:
            res = func(*args, **kwargs)
        except Exception as ex:
            print(f"Problem occured during the execution of {func}\n{ex}")
            return None

        try:
            WebDriverWait(DRIVER, SLEEP_PAGE_REFRESH).until(expected_conditions.staleness_of(old_page))
        except TimeoutException as _:
            print("Time limit for refresh has run out. Is AJAX present?")
        except Exception as ex:
            print(f"Something went wrong while waiting for page to refresh\n{ex}")
            return None
        return res

    return execute_func_and_wait


# can be used both as context manager and decorator!
# you can't return the value of the passed function when in decorator mode
@contextmanager
def wait_page_refresh_context_manager():
    try:
        WebDriverWait(DRIVER, SLEEP_FOR_WAITS).until(
                expected_conditions.presence_of_element_located((By.TAG_NAME, 'html')))
        old_page = DRIVER.find_element(By.TAG_NAME, 'html')
    except TimeoutException as ex:
        print(f"html tag did not appear in time\n{ex}")
        raise
    except NoSuchElementException as ex:
        print(f"Can't locate the 'html' tag\n{ex}")
        raise
    # go back and process actions
    yield
    try:
        WebDriverWait(DRIVER, SLEEP_PAGE_REFRESH).until(expected_conditions.staleness_of(old_page))
    except TimeoutException as _:
        print("Time limit for refresh has run out. Is AJAX present?")
    except Exception as ex:
        print(f"Something went wrong while waiting for page to refresh\n{ex}")
        raise


def wait_appear_xpath(xpath: str):
    try:
        elem = WebDriverWait(DRIVER, SLEEP_FOR_WAITS). \
            until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))

    except TimeoutException as ex:
        print(f"Element with path {xpath} did not appear\n{ex}")
        return None

    return elem


def wait_clickable_xpath(xpath: str):
    try:
        found_elem = WebDriverWait(DRIVER, SLEEP_FOR_WAITS). \
            until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))

    except TimeoutException as ex:
        print(f"Element with path {xpath} did not become clickable\n{ex}")
        return None

    return found_elem
