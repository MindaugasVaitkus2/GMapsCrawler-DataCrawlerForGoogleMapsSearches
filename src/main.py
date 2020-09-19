
import os
import time
from helpers import *

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options

def get_current_url():
    return driver.current_url

def set_current_url(url_str):
    driver.get(url_str)

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

    url = 'https://www.google.com.br/maps/search/a/'
    url = set_gmaps_url_search_str(url, search_str)
    print(url)
    driver.get(url)

    time.sleep(2)
    search_places_str = []
    page_places = []
    has_next_page = True
    while(has_next_page):
        time.sleep(2)
        page_places = get_gmaps_search_page_places()
        for page_place in page_places:
            search_places_str.append(page_place.text)
        has_next_page = goto_gmaps_search_next_page()
    return search_places_str

def get_gmaps_place(search_str, place_str):

    url = 'https://www.google.com.br/maps/search/a/'
    url = set_gmaps_url_search_str(url, search_str + ' ' + place_str)
    print(url)
    driver.get(url)

    time.sleep(2)
    has_target_found = False
    has_next_page = True
    while(has_next_page):
        time.sleep(2)
        page_places = get_gmaps_search_page_places()
        for page_place in page_places:
            print(page_place.text)
            print(target_str)
            print(page_place.text == target_str)
            print(' ')
            if(page_place.text == target_str):
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

if __name__ == '__main__':

    # examples of 'search string' and 'place string'
    search_str = 'petrolina pizzaria'
    place_str = 'Pizzaria Jecana'

    # uses search string to get a list of places strings
    search_places_str = get_gmaps_places_str(search_str)
    print(search_places_str)
    time.sleep(2)

    # uses search string and a place string to get a dict about the place
    get_gmaps_place(search_str, place_str)
    time.sleep(10)

    driver.quit()