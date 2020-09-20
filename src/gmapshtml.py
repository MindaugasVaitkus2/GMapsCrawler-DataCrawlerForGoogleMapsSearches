
from abc import ABC

import time
from browser import Browser
from gmapsurl import GMapsURL

from selenium.common import exceptions

class GMapsHTML(ABC):

    @staticmethod
    def get_search_page_places(driver):
        search_page_places = driver.find_elements_by_class_name("section-result-title")
        return search_page_places

    @staticmethod
    def goto_search_next_page(driver):
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

    @staticmethod
    def get_places_str(driver, GMAPS_URL, search_str):

        # assemply and request an initial gmaps url using a search string
        url = GMapsURL.set_search_str(GMAPS_URL, search_str)
        Browser.set_url(driver, url)

        time.sleep(2)
        search_places_str = []
        has_next_page = True
        while(has_next_page):
            time.sleep(2)
            page_places_str = GMapsHTML.get_search_page_places(driver)
            for page_place in page_places_str:
                search_places_str.append(page_place.text)
            has_next_page = GMapsHTML.goto_search_next_page(driver)
        return search_places_str

    @staticmethod
    def get_place(driver, GMAPS_URL, search_str, place_str):

        # assemply and request an initial gmaps url using a search and place strings
        url = GMapsURL.set_search_str(GMAPS_URL, search_str + ' ' + place_str)
        Browser.set_url(driver, url)

        time.sleep(2)
        has_target_found = False
        has_next_page = True
        while(has_next_page):
            time.sleep(2)
            page_places = GMapsHTML.get_search_page_places(driver)
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
                has_next_page = GMapsHTML.goto_search_next_page(driver)