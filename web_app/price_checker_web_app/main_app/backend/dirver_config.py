from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

CHROME_OPTIONS = Options()
# CHROME_OPTIONS.add_experimental_option("detach", True)
CHROME_OPTIONS.add_argument("start-maximized")
DRIVER = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=CHROME_OPTIONS)
MAX_SCRIPT_REPEAT = 20
