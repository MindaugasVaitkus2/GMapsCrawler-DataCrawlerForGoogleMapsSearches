
import os
import time

from browser import Browser
from gmapsurl import GMapsURL

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions

class GMapsCrawler():

    DRIVER = None
    GMAPS_URL = None

    def __init__(self):
        pass

    def get_results_n(self):
        elements_found = self.DRIVER.find_elements_by_class_name("section-result-title")
        return len(elements_found)

    def collect_search_page_results(self):
        elements_found = self.DRIVER.find_elements_by_class_name("section-result-title")
        search_page_results = []
        for element in elements_found:
            search_page_results.append({ 'title': element.text })
        return search_page_results

    def collect_title(self):
        elements_found = self.DRIVER.find_elements_by_class_name("section-hero-header-title-title")
        texts_found = []
        for element in elements_found:
            texts_found.append({'value': element.text})
        if(len(texts_found) > 0):
            return texts_found[0]
        else:
            return {'value': None }

    def collect_address(self):
        elements_found = self.DRIVER.find_elements_by_class_name("ugiz4pqJLAG__primary-text")
        texts_found = []
        for element in elements_found:
            texts_found.append({'value': element.text})
        if(len(texts_found) > 0):
            return texts_found[0]
        else:
            return {'value': None }

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

    def get_titles(self, search_str):

        STATE = 'CREATING_SESSION'
        has_next_page = True
        debug_mode = False
        titles = []

        while(True):

            if(STATE == 'CREATING_SESSION'):

                # STATE behavior          
                CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']
                CHROME_OPTIONS = webdriver.ChromeOptions() #Options()
                CHROME_OPTIONS.add_argument("--user-data-dir=.\chrome-data")
                CHROME_OPTIONS.add_argument("--enable-automation")
                #CHROME_OPTIONS.add_argument("--window-size=800,600")
                #CHROME_OPTIONS.add_argument("start-maximized");
                self.DRIVER = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=CHROME_OPTIONS)
                self.GMAPS_URL = 'https://www.google.com/maps/'

                # transition logic
                STATE = 'ACCESSING_GMAPS_URL'

            elif(STATE == 'ACCESSING_GMAPS_URL'):
                if(debug_mode): print(STATE)

                # STATE behavior
                url = GMapsURL.set_search_str(self.GMAPS_URL, search_str)
                Browser.set_url(self.DRIVER, url)
                time.sleep(2)

                # transition logic
                url = Browser.get_url(self.DRIVER)
                if(self.has_title()):
                    STATE = 'COLLECTING_SINGLE_RESULT'
                elif(GMapsURL.is_search_page(url)):
                    STATE = 'COLLECTING_PAGE_RESULTS'
                else:
                    STATE = 'FAIL'

            elif(STATE == 'COLLECTING_PAGE_RESULTS'):
                if(debug_mode): print(STATE)

                # STATE behavior                
                search_page_results = self.collect_search_page_results()
                for search_page_result in search_page_results:
                    titles.append(search_page_result)
                time.sleep(2)

                # transition logic
                STATE = 'GOING_TO_NEXT_PAGE'

            elif(STATE == 'COLLECTING_SINGLE_RESULT'):
                if(debug_mode): print(STATE)
                
                # STATE behavior
                self.hit_searchbox_button()
                time.sleep(2)
                for _ in range(21):
                    self.hit_zoom_in()
                time.sleep(2)

                url = Browser.get_url(self.DRIVER)
                finding = {
                    "title": self.collect_title()['value'] 
                }
                titles.append(finding)
                if(debug_mode): print(titles)

                # transition logic
                STATE = 'FINISH'

            elif(STATE == 'GOING_TO_NEXT_PAGE'):
                if(debug_mode): print(STATE)

                # STATE behavior
                self.access_search_back_to_results()
                time.sleep(2)
                has_next_page = self.access_search_next_page()
                time.sleep(2)

                # transition logic
                if(has_next_page):
                    STATE = 'COLLECTING_PAGE_RESULTS'
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

        Browser.quit(self.DRIVER)
        return titles

    def get_places(self, search_str):

        STATE = 'CREATING_SESSION'
        PAGE_CURSOR = 0
        PAGE_CURSOR_LIMIT = None
        has_next_page = True

        debug_mode = False

        findings = []

        while(True):

            if(STATE == 'CREATING_SESSION'):
    
                # STATE behavior          
                CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']
                CHROME_OPTIONS = webdriver.ChromeOptions() #Options()
                CHROME_OPTIONS.add_argument("--user-data-dir=.\chrome-data")
                CHROME_OPTIONS.add_argument("--enable-automation")
                #CHROME_OPTIONS.add_argument("--window-size=800,600")
                #CHROME_OPTIONS.add_argument("start-maximized");
                self.DRIVER = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=CHROME_OPTIONS)
                self.GMAPS_URL = 'https://www.google.com/maps/'

                # transition logic
                STATE = 'ACCESSING_GMAPS_URL'

            elif(STATE == 'ACCESSING_GMAPS_URL'):
                if(debug_mode): print(STATE)

                # STATE behavior
                url = GMapsURL.set_search_str(self.GMAPS_URL, search_str)
                Browser.set_url(self.DRIVER, url)
                time.sleep(2)

                # transition logic
                url = Browser.get_url(self.DRIVER)
                if(self.has_title()):
                    STATE = 'COLLECTING_SINGLE_RESULT'
                elif(GMapsURL.is_search_page(url)):
                    STATE = 'COLLECTING_PAGE_RESULTS'
                else:
                    STATE = 'FAIL'

            elif(STATE == 'COLLECTING_PAGE_RESULTS'):
                if(debug_mode): print(STATE)

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
                if(debug_mode): print(STATE)

                # STATE behavior
                url = Browser.get_url(self.DRIVER)
                finding = {
                    "place": { 
                        "title": self.collect_title()['value'], 
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

                if(debug_mode): print(finding)
         
                # transition logic
                PAGE_CURSOR += 1
                STATE = 'RETURNING_TO_LIST'

            elif(STATE == 'COLLECTING_SINGLE_RESULT'):
                if(debug_mode): print(STATE)
                
                # STATE behavior
                self.hit_searchbox_button()
                time.sleep(2)
                for _ in range(21):
                    self.hit_zoom_in()
                time.sleep(2)

                url = Browser.get_url(self.DRIVER)
                finding = {
                    "place": { 
                        "title": self.collect_title()['value'], 
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
                if(debug_mode): print(findings)

                # transition logic
                STATE = 'FINISH'

            elif(STATE == 'RETURNING_TO_LIST'):
                if(debug_mode): print(STATE)
    
                # STATE behavior
                self.access_search_back_to_results()
                time.sleep(2)
                for _ in range(21):
                    self.hit_zoom_in()
                time.sleep(2)

                # transition logic
                STATE = 'COLLECTING_PAGE_RESULTS'

            elif(STATE == 'GOING_TO_NEXT_PAGE'):
                if(debug_mode): print(STATE)

                # STATE behavior
                self.access_search_back_to_results()
                time.sleep(2)
                has_next_page = self.access_search_next_page()
                time.sleep(2)

                # transition logic
                if(has_next_page):
                    STATE = 'COLLECTING_PAGE_RESULTS'
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

        Browser.quit(self.DRIVER)
        return findings