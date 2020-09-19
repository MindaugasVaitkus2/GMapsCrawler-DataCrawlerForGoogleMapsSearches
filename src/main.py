
import os
import time
from helpers import *

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options

def get_gmaps_search_page_itens():
    search_page_itens = driver.find_elements_by_class_name("section-result-title")
    return search_page_itens

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

def get_gmaps_itens_str(search_str):

    url = 'https://www.google.com.br/maps/search/a/'
    url = set_gmaps_url_search_str(url, search_str)
    print(url)
    driver.get(url)

    time.sleep(2)
    search_itens_str = []
    page_itens = []
    has_next_page = True
    while(has_next_page):
        time.sleep(2)
        page_itens = get_gmaps_search_page_itens()
        for page_item in page_itens:
            search_itens_str.append(page_item.text)
        has_next_page = goto_gmaps_search_next_page()
    return search_itens_str

def get_gmaps_item(search_str, item_str):

    url = 'https://www.google.com.br/maps/search/a/'
    url = set_gmaps_url_search_str(url, search_str + ' ' + item_str)
    print(url)
    driver.get(url)

    time.sleep(2)
    has_target_found = False
    has_next_page = True
    while(has_next_page):
        time.sleep(2)
        page_itens = get_gmaps_search_page_itens()
        for page_item in page_itens:
            print(page_item.text)
            print(target_str)
            print(page_item.text == target_str)
            print(' ')
            if(page_item.text == target_str):
                has_target_found = True
                has_next_page = False    
                time.sleep(2)            
                #driver.get('https://www.google.com.br/maps/search/petrolina+pizzaria//@0.0,0.0,21z/')
                #time.sleep(2) 
                page_item.click()
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

    search_str = 'petrolina pizzaria'
    item_str = 'Pizzaria Jecana'

    search_itens_str = get_gmaps_itens_str(search_str)
    print(search_itens_str)
    time.sleep(2)

    get_gmaps_item(search_str, item_str)
    time.sleep(10)

    driver.quit()