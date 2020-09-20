
import time
from browser import Browser
from gmapsurl import GMapsURL

from selenium.common import exceptions

class GMapsNav():

    driver = None
    GMAPS_URL = None

    def __init__(self, driver, GMAPS_URL):
        self.driver = driver
        self.GMAPS_URL = GMAPS_URL

    def get_search_page_spots(self):
        search_page_spots = self.driver.find_elements_by_class_name("section-result-title")
        return search_page_spots

    def goto_search_next_page(self):
        possible_enabled_target_elements = self.driver.find_elements_by_id('n7lv7yjyC35__section-pagination-button-next')
        try:
            possible_enabled_target_elements[0].click()
            return True
        except exceptions.ElementClickInterceptedException:
            return False
        except exceptions.ElementNotInteractableException:
            return False
        except exceptions.StaleElementReferenceException:
            return False

    def get_spots_str(self, search_str):

        # assemply and request an initial gmaps url using a search string
        url = GMapsURL.set_search_str(self.GMAPS_URL, search_str)
        Browser.set_url(self.driver, url)

        time.sleep(2)
        search_spots_str = []
        has_next_page = True
        while(has_next_page):
            time.sleep(2)
            page_spots_str = self.get_search_page_spots()
            for page_spot in page_spots_str:
                search_spots_str.append(page_spot.text)
            has_next_page = self.goto_search_next_page()
        return search_spots_str

    def get_spot(self, search_str, spot_str):

        # assemply and request an initial gmaps url using a search and spot strings
        url = GMapsURL.set_search_str(self.GMAPS_URL, search_str + ' ' + spot_str)
        Browser.set_url(driver, url)

        time.sleep(2)
        has_target_found = False
        has_next_page = True
        while(has_next_page):
            time.sleep(2)
            page_spots = self.get_search_page_spots()
            for page_spot in page_spots:
                print(page_spot.text)
                print(spot_str)
                print(page_spot.text == spot_str)
                print(' ')
                if(page_spot.text == spot_str):
                    has_target_found = True
                    has_next_page = False    
                    time.sleep(2)            
                    #driver.get('https://www.google.com.br/maps/search/petrolina+pizzaria//@0.0,0.0,21z/')
                    #time.sleep(2) 
                    page_spot.click()
                    time.sleep(2)
                    break
            if(not has_target_found):
                has_next_page = self.goto_search_next_page()

