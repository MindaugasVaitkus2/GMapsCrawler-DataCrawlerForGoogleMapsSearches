
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

DRIVER = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=CHROME_OPTIONS)
GMAPS_URL = 'https://www.google.com/maps/'

if __name__ == '__main__':

    # examples of search and place strings
    search_str = 'petrolina pizzaria'
    place_str = ''

    # GMapsNav instatiation
    gmaps = GMapsNav(DRIVER, GMAPS_URL)

    # uses search string to get a list of places strings
    #places_str = gmaps.get_search_results(search_str)
    #print(places_str)
    #time.sleep(5)

    # uses search string and a place string to get a dict about the place
    gmaps.get_place(search_str, place_str)


