
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

    def get_search_page_results(self):
        elements_found = self.DRIVER.find_elements_by_class_name("section-result-title")
        search_page_results = []
        for element in elements_found:
            search_page_results.append({'search-index': None, 'place': element.text})
        return search_page_results

    def goto_search_next_page(self):
        possible_enabled_target_elements = self.DRIVER.find_elements_by_id('n7lv7yjyC35__section-pagination-button-next')
        try:
            possible_enabled_target_elements[0].click()
            return True
        except Exception as e:
            #print(e)
            return False

    def get_search_results(self, search_str):

        STATE = 'ACCESSING_GMAPS_URL'
        search_results = []
        has_next_page = True

        while(True):

            if(STATE == 'ACCESSING_GMAPS_URL'):
    
                # STATE behavior
                url = GMapsURL.set_search_str(self.GMAPS_URL, search_str)
                Browser.set_url(self.DRIVER, url)
                time.sleep(2)

                # transition logic
                url = Browser.get_url(self.DRIVER)
                if(GMapsURL.is_search_page(url)):
                    STATE = 'GETTING_PAGE_RESULTS'
                elif(GMapsURL.is_place_page(url)):
                    STATE = 'GETTING_SINGLE_RESULT'
                else:
                    STATE = 'FAIL'
            
            elif(STATE == 'GETTING_PAGE_RESULTS'):

                # STATE behavior                
                search_page_results = self.get_search_page_results()
                for search_page_result in search_page_results:
                    search_results.append(search_page_result)
                has_next_page = self.goto_search_next_page()
                time.sleep(2)

                # transition logic
                if(has_next_page):
                    STATE = 'GETTING_PAGE_RESULTS'
                elif(not has_next_page):
                    STATE = 'FINISH'
                else:
                    STATE = 'FAIL'

            elif(STATE == 'GETTING_SINGLE_RESULT'):
                # do something for GETTING_SINGLE_RESULT STATE
                break

            elif(STATE == 'FINISH'):
                # do something for FINISH STATE
                break

            elif(STATE == 'FAIL'):
                # do something for FAIL STATE
                break

        Browser.close(self.DRIVER)

        for i, search_result in enumerate(search_results, start=1):
            search_result['search-index'] = i

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
            page_places = self.get_search_page_results()
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
