
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

    def get_results_n(self):
        elements_found = self.DRIVER.find_elements_by_class_name("section-result-title")
        return len(elements_found)

    def collect_search_page_results(self):
        elements_found = self.DRIVER.find_elements_by_class_name("section-result-title")
        search_page_results = []
        for element in elements_found:
            search_page_results.append({'search-index': None, 'place': element.text})
        return search_page_results

    def access_search_page_result_by_index(self, index):
        possible_enabled_target_elements = self.DRIVER.find_elements_by_class_name('section-result-text-content')
        try:
            possible_enabled_target_elements[index].click()
            return True
        except Exception as e:
            #print(e)
            return False

    def access_search_next_page(self):
        possible_enabled_target_elements = self.DRIVER.find_elements_by_id('n7lv7yjyC35__section-pagination-button-next')
        try:
            possible_enabled_target_elements[0].click()
            return True
        except Exception as e:
            #print(e)
            return False

    def access_search_back_to_results(self):
        possible_enabled_target_elements = self.DRIVER.find_elements_by_class_name('section-back-to-list-button')
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
                search_page_results = self.collect_search_page_results()
                for search_page_result in search_page_results:
                    search_results.append(search_page_result)
                has_next_page = self.access_search_next_page()
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

        STATE = 'ACCESSING_GMAPS_URL'
        PAGE_CURSOR = 0
        PAGE_RESULTS_LIMIT = None
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
                    STATE = 'ACCESSING_CURSOR_RESULT'
                elif(GMapsURL.is_place_page(url)):
                    STATE = 'GETTING_SINGLE_RESULT'
                else:
                    STATE = 'FAIL'
            
            elif(STATE == 'ACCESSING_CURSOR_RESULT'):

                # STATE behavior
                self.access_search_page_result_by_index(PAGE_CURSOR)
                PAGE_RESULTS_LIMIT = self.get_results_n() - 1          
                print(PAGE_RESULTS_LIMIT)
                print(PAGE_CURSOR)  
                print('')  
                time.sleep(2)

                # transition logic
                STATE = 'COLLECTING_RESULT'

            elif(STATE == 'COLLECTING_RESULT'):
        
                # STATE behavior
                PAGE_CURSOR += 1


                # transition logic
                if(PAGE_CURSOR <= PAGE_RESULTS_LIMIT):
                    STATE = 'RETURNING_TO_LIST'
                else:
                    STATE = 'GOING_TO_NEXT_PAGE'

            elif(STATE == 'RETURNING_TO_LIST'):
    
                # STATE behavior
                self.access_search_back_to_results()
                time.sleep(2)

                # transition logic
                STATE = 'ACCESSING_CURSOR_RESULT'

            elif(STATE == 'GOING_TO_NEXT_PAGE'):

                 # STATE behavior
                self.access_search_back_to_results()
                time.sleep(2)
                has_next_page = self.access_search_next_page()
                time.sleep(2)

                # transition logic
                if(has_next_page):
                    STATE = 'ACCESSING_CURSOR_RESULT'
                    PAGE_CURSOR = 1
                else:
                    STATE = 'FINISH'

            elif(STATE == 'FINISH'):
                # do something for FINISH STATE
                break

            elif(STATE == 'FAIL'):
                # do something for FAIL STATE
                break

        Browser.close(self.DRIVER)