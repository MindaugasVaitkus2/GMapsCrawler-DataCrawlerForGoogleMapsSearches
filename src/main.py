
import os
import time

from browser import Browser
from gmapsurl import GMapsURL
from gmapsnav import GMapsNav

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']
CHROME_OPTIONS = webdriver.ChromeOptions() #Options()
CHROME_OPTIONS.add_argument("--user-data-dir=.\chrome-data")
CHROME_OPTIONS.add_argument("--enable-automation")

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=CHROME_OPTIONS)
GMAPS_URL = 'https://www.google.com/maps/'

if __name__ == '__main__':

    # examples of search and place strings
    search_str = 'petrolina pizzaria'
    spot_str = 'Pizzaria Jecana'

    # uses search string to get a list of places strings
    search_places_str = GMapsNav.get_spots_str(driver, GMAPS_URL, search_str)
    print(search_places_str)
    time.sleep(5)

    # uses search string and a place string to get a dict about the place
    #GMapsNav.get_place(driver, GMAPS_URL, search_str, spot_str)
    #time.sleep(10)

    driver.quit()