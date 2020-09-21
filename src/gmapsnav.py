
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
        #self.gmapsauto = GMapsAuto(DRIVER, GMAPS_URL)

    def get_results_n(self):
        elements_found = self.DRIVER.find_elements_by_class_name("section-result-title")
        return len(elements_found)

    def collect_search_page_results(self):
        elements_found = self.DRIVER.find_elements_by_class_name("section-result-title")
        search_page_results = []
        for element in elements_found:
            search_page_results.append({'search-index': None, 'place': element.text})
        return search_page_results

    def collect_place(self):
        elements_found = self.DRIVER.find_elements_by_class_name("section-hero-header-title-title")
        texts_found = []
        for element in elements_found:
            texts_found.append({'value': element.text})
        return texts_found[0]

    def collect_address(self):
        elements_found = self.DRIVER.find_elements_by_class_name("ugiz4pqJLAG__primary-text")
        texts_found = []
        for element in elements_found:
            texts_found.append({'value': element.text})
        return texts_found[0]

    def collect_status(self):
        elements_found = self.DRIVER.find_elements_by_class_name("cX2WmPgCkHi__section-info-text")
        texts_found = []
        for element in elements_found:
            texts_found.append({'value': element.text})
        if(len(texts_found) > 0):
            return texts_found[0]
        else:
            return {'value': None }

    def collect_phone(self):
        elements_found = self.DRIVER.find_elements_by_class_name("ugiz4pqJLAG__primary-text")
        texts_found = []
        for element in elements_found:
            texts_found.append({'value': element.text})
        if(len(texts_found) > 0):
            return texts_found[0]
        else:
            return {'value': None }

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

    def hit_zoom_in(self):
        possible_enabled_target_elements = self.DRIVER.find_elements_by_id('widget-zoom-in')
        try:
            possible_enabled_target_elements[0].click()
            return True
        except Exception as e:
            #print(e)
            return False        

    def hit_zoom_out(self):
        possible_enabled_target_elements = self.DRIVER.find_elements_by_id('widget-zoom-out')
        try:
            possible_enabled_target_elements[0].click()
            return True
        except Exception as e:
            #print(e)
            return False   

    def hit_searchbox_button(self):
        possible_enabled_target_elements = self.DRIVER.find_elements_by_id('searchbox-searchbutton')
        try:
            possible_enabled_target_elements[0].click()
            return True
        except Exception as e:
            #print(e)
            return False   

    def has_title(self):
        elements_found = self.DRIVER.find_elements_by_class_name("section-hero-header-title-title")
        if(len(elements_found) > 0):
            return True
        else:
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
                    STATE = 'COLLECTING_SINGLE_RESULT'
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

            elif(STATE == 'COLLECTING_SINGLE_RESULT'):
                # do something for COLLECTING_SINGLE_RESULT STATE
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
        PAGE_CURSOR_LIMIT = None
        has_next_page = True

        debug_mode = True

        findings = []

        while(True):

            if(STATE == 'ACCESSING_GMAPS_URL'):
                if(debug_mode): print('ACCESSING_GMAPS_URL')

                # STATE behavior
                url = GMapsURL.set_search_str(self.GMAPS_URL, search_str)
                Browser.set_url(self.DRIVER, url)
                time.sleep(2)

                # transition logic
                url = Browser.get_url(self.DRIVER)
                if(self.has_title()):
                    STATE = 'COLLECTING_SINGLE_RESULT'
                elif(GMapsURL.is_search_page(url)):
                    STATE = 'ACCESSING_CURSOR_RESULT'
                else:
                    STATE = 'FAIL'

            elif(STATE == 'ACCESSING_CURSOR_RESULT'):
                if(debug_mode): print('ACCESSING_CURSOR_RESULT')

                # STATE behavior
                self.access_search_page_result_by_index(PAGE_CURSOR)
                PAGE_CURSOR_LIMIT = self.get_results_n() - 1          
                #print(PAGE_CURSOR_LIMIT)
                #print(PAGE_CURSOR)  
                #print('')  
                time.sleep(2)

                # transition logic
                if(PAGE_CURSOR <= PAGE_CURSOR_LIMIT):
                    STATE = 'COLLECTING_CURSOR_RESULT'
                else:
                    STATE = 'GOING_TO_NEXT_PAGE'

            elif(STATE == 'COLLECTING_CURSOR_RESULT'):
                if(debug_mode): print('COLLECTING_CURSOR_RESULT')

                # STATE behavior
                url = Browser.get_url(self.DRIVER)
                finding = {
                    "place": { 
                        "name": self.collect_place()['value'], 
                        "address": self.collect_address()['value'],
                        #"contact": {
                        #    "phone": self.collect_phone()['value']
                        #},                      
                        "status": self.collect_status()['value'],
                        "coordinates": {
                            "latitude": GMapsURL.get_cursor(url)['lat'],
                            "longitude": GMapsURL.get_cursor(url)['lon'] + 0.0001364
                        } 
                    }
                }
                findings.append(finding)
                time.sleep(2)

                print(finding)
         
                # transition logic
                PAGE_CURSOR += 1
                STATE = 'RETURNING_TO_LIST'

            elif(STATE == 'COLLECTING_SINGLE_RESULT'):
                if(debug_mode): print('COLLECTING_SINGLE_RESULT')
                
                # STATE behavior
                self.hit_searchbox_button()
                time.sleep(2)
                for _ in range(21):
                    self.hit_zoom_in()
                time.sleep(2)

                url = Browser.get_url(self.DRIVER)
                finding = {
                    "place": { 
                        "name": self.collect_place()['value'], 
                        "address": self.collect_address()['value'],
                        #"contact": {
                        #    "phone": self.collect_phone()['value']
                        #},                      
                        "status": self.collect_status()['value'],
                        "coordinates": {
                            "latitude": GMapsURL.get_cursor(url)['lat'],
                            "longitude": GMapsURL.get_cursor(url)['lon'] + 0.0001364
                        } 
                    }
                }
                findings.append(finding)
                print(findings)

                # transition logic
                STATE = 'FINISH'

            elif(STATE == 'RETURNING_TO_LIST'):
                if(debug_mode): print('RETURNING_TO_LIST')
    
                # STATE behavior
                self.access_search_back_to_results()
                time.sleep(2)
                for _ in range(21):
                    self.hit_zoom_in()
                time.sleep(2)

                # transition logic
                STATE = 'ACCESSING_CURSOR_RESULT'

            elif(STATE == 'GOING_TO_NEXT_PAGE'):
                if(debug_mode): print('GOING_TO_NEXT_PAGE')

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
                if(debug_mode): print('FINISH')
                # do something for FINISH STATE
                break

            elif(STATE == 'FAIL'):
                if(debug_mode): print('FAIL')
                # do something for FAIL STATE
                break

        Browser.close(self.DRIVER)