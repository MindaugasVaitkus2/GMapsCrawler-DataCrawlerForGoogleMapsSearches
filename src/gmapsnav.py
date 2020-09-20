
import time
from browser import Browser
from gmapsurl import GMapsURL

from selenium.common import exceptions

class GMapsNav():

    DRIVER = None
    GMAPS_URL = None

    def __init__(self, DRIVER, GMAPS_URL):
        self.DRIVER = DRIVER
        self.GMAPS_URL = GMAPS_URL

    def get_search_page_places(self):
        search_page_places = self.DRIVER.find_elements_by_class_name("section-result-title")
        return search_page_places

    def goto_search_next_page(self):
        possible_enabled_target_elements = self.DRIVER.find_elements_by_id('n7lv7yjyC35__section-pagination-button-next')
        try:
            possible_enabled_target_elements[0].click()
            return True
        except exceptions.ElementClickInterceptedException:
            return False
        except exceptions.ElementNotInteractableException:
            return False
        except exceptions.StaleElementReferenceException:
            return False

    def get_search_results(self, search_str):

        state = 'GETTING_URL'
        search_places_str = []
        has_next_page = True

        while(True):

            if(state == 'GETTING_URL'):

                # state behavior
                url = GMapsURL.set_search_str(self.GMAPS_URL, search_str)
                Browser.set_url(self.DRIVER, url)
                time.sleep(2)

                # transition logic
                url = Browser.get_url(self.DRIVER)
                if(GMapsURL.is_search_page(url)):
                    state = 'SEARCHING_RESULTS'
                elif(GMapsURL.is_place_page(url)):
                    state = 'GETTING_SINGLE_RESULT'
                else:
                    state = 'FAIL'
                    break
            
            elif(state == 'SEARCHING_RESULTS'):

                # state behavior                
                page_places_str = self.get_search_page_places()
                for page_place in page_places_str:
                    search_places_str.append(page_place.text)
                has_next_page = self.goto_search_next_page()
                time.sleep(2)

                # transition logic
                if(has_next_page):
                    state = 'SEARCHING_RESULTS'
                elif(not has_next_page):
                    state = 'FINISH'
                    break
                else:
                    state = 'FAIL'
                    break

        Browser.close(self.DRIVER)

        #return search_places_str

        search_results = []
        for i, place_str in enumerate(search_places_str):
            search_results.append({'index': i, 'place': place_str})

        return search_results

    def get_place(self, search_str, place_str):

        # assemply and request an initial gmaps url using a search and place strings
        url = GMapsURL.set_search_str(self.GMAPS_URL, search_str + ' ' + place_str)
        Browser.set_url(self.DRIVER, url)

        time.sleep(2)
        has_target_found = False
        has_next_page = True
        while(has_next_page):
            time.sleep(2)
            page_places = self.get_search_page_places()
            for page_place in page_places:
                print(page_place.text)
                print(place_str)
                print(page_place.text == place_str)
                print(' ')
                if(page_place.text == place_str):
                    has_target_found = True
                    has_next_page = False    
                    time.sleep(2)            
                    #DRIVER.get('https://www.google.com.br/maps/search/petrolina+pizzaria//@0.0,0.0,21z/')
                    #time.sleep(2) 
                    page_place.click()
                    time.sleep(2)
                    break
            if(not has_target_found):
                has_next_page = self.goto_search_next_page()

        Browser.close(self.DRIVER)
