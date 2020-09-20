
import os
import time

from browser_handler import *
from gmaps_url_handler import *
from gmaps_html_handler import *

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options

def get_gmaps_search_page_places():
    search_page_places = driver.find_elements_by_class_name("section-result-title")
    return search_page_places

def goto_gmaps_search_next_page():
    possible_enabled_target_elements = driver.find_elements_by_id('n7lv7yjyC35__section-pagination-button-next')
    try:
        possible_enabled_target_elements[0].click()
        return True
    except exceptions.ElementClickInterceptedException:
        return False
    except exceptions.ElementNotInteractableException:
        return False
    except exceptions.StaleElementReferenceException:
        return False

def get_gmaps_places_str(search_str):

    # assemply and request an initial gmaps url using a search string
    url = set_gmaps_url_search_str(GMAPS_URL, search_str)
    driver.get(url)

    time.sleep(2)
    search_places_str = []
    has_next_page = True
    while(has_next_page):
        time.sleep(2)
        page_places_str = get_gmaps_search_page_places()
        for page_place in page_places_str:
            search_places_str.append(page_place.text)
        has_next_page = goto_gmaps_search_next_page()
    return search_places_str

def get_gmaps_place(search_str, place_str):

    # assemply and request an initial gmaps url using a search and place strings
    url = set_gmaps_url_search_str(GMAPS_URL, search_str + ' ' + place_str)
    driver.get(url)

    time.sleep(2)
    has_target_found = False
    has_next_page = True
    while(has_next_page):
        time.sleep(2)
        page_places = get_gmaps_search_page_places()
        for page_place in page_places:
            print(page_place.text)
            print(place_str)
            print(page_place.text == place_str)
            print(' ')
            if(page_place.text == place_str):
                has_target_found = True
                has_next_page = False    
                time.sleep(2)            
                #driver.get('https://www.google.com.br/maps/search/petrolina+pizzaria//@0.0,0.0,21z/')
                #time.sleep(2) 
                page_place.click()
                time.sleep(2)
                break
        if(not has_target_found):
            has_next_page = goto_gmaps_search_next_page()


CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']
CHROME_OPTIONS = webdriver.ChromeOptions() #Options()
CHROME_OPTIONS.add_argument("--user-data-dir=.\chrome-data")
CHROME_OPTIONS.add_argument("--enable-automation")
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=CHROME_OPTIONS)

GMAPS_URL = 'https://www.google.com/maps/'

if __name__ == '__main__':

    # examples of search and place strings
    search_str = 'petrolina pizzaria'
    place_str = 'Pizzaria Jecana'

    # uses search string to get a list of places strings
    search_places_str = get_gmaps_places_str(search_str)
    print(search_places_str)
    time.sleep(5)

    # uses search string and a place string to get a dict about the place
    #get_gmaps_place(search_str, place_str)
    #time.sleep(10)

    driver.quit()