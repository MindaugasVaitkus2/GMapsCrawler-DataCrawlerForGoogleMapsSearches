
import os
import time

from browserhandler import BrowserHandler
from gmapshandler import GMapsHandler
from gmapsurlassembler import GMapsURLAssembler

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions

import pandas as pd

class GMapsCrawler():

    DRIVER = None
    GMAPS_URL = None
    DEBUG_MODE = None

    def __init__(self, debug=False, delay=2):
        self.GMAPS_URL = 'https://www.google.com/maps/'
        self.DEBUG_MODE = debug
        self.DEFAULT_DELAY = delay
        self.CORRECTION_FACTOR = 0.0001364

    def get_titles(self, search_str):

        STATE = 'CREATING_SESSION'
        titles = []

        while(True):

            if(STATE == 'CREATING_SESSION'):

                # STATE behavior
                if(self.DEBUG_MODE):
                    CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']
                    CHROME_OPTIONS = Options()
                    #CHROME_OPTIONS.add_argument("--user-data-dir=.\chrome-data")
                    CHROME_OPTIONS.add_argument("--enable-automation");
                    self.DRIVER = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=CHROME_OPTIONS)
                else:
                    CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']
                    CHROME_OPTIONS = Options()
                    CHROME_OPTIONS.add_argument('--headless')
                    CHROME_OPTIONS.add_argument('--disable-gpu')  # Last I checked this was necessary.
                    self.DRIVER = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=CHROME_OPTIONS)

                # transition logic
                STATE = 'ACCESSING_GMAPS_URL'

            elif(STATE == 'ACCESSING_GMAPS_URL'):
                if(self.DEBUG_MODE): print(STATE)

                # STATE behavior
                url = GMapsURLAssembler.set_search_str(self.GMAPS_URL, search_str)
                BrowserHandler.set_url(self.DRIVER, url)
                time.sleep(self.DEFAULT_DELAY)

                # transition logic
                url = BrowserHandler.get_url(self.DRIVER)
                if(GMapsHandler.has_title(self.DRIVER)):
                    STATE = 'COLLECTING_SINGLE_RESULT'
                elif(GMapsURLAssembler.is_search_page(url)):
                    STATE = 'COLLECTING_PAGE_RESULTS'
                else:
                    STATE = 'FAIL'

            elif(STATE == 'COLLECTING_PAGE_RESULTS'):
                if(self.DEBUG_MODE): print(STATE)

                # STATE behavior                
                search_page_results = GMapsHandler.collect_search_page_results(self.DRIVER)
                for search_page_result in search_page_results:
                    titles.append(search_page_result)
                time.sleep(self.DEFAULT_DELAY)

                # transition logic
                STATE = 'GOING_TO_NEXT_PAGE'

            elif(STATE == 'COLLECTING_SINGLE_RESULT'):
                if(self.DEBUG_MODE): print(STATE)
                
                # STATE behavior
                GMapsHandler.hit_searchbox_button(self.DRIVER)
                time.sleep(self.DEFAULT_DELAY)
                for _ in range(21):
                    GMapsHandler.hit_zoom_in(self.DRIVER)
                time.sleep(self.DEFAULT_DELAY)

                url = BrowserHandler.get_url(self.DRIVER)
                title = {
                    "title": GMapsHandler.collect_title(self.DRIVER)['value'] 
                }
                titles.append(title)
                if(self.DEBUG_MODE): print(titles)

                # transition logic
                STATE = 'FINISH'

            elif(STATE == 'GOING_TO_NEXT_PAGE'):
                if(self.DEBUG_MODE): print(STATE)

                # STATE behavior
                GMapsHandler.access_search_back_to_results(self.DRIVER)
                time.sleep(self.DEFAULT_DELAY)
                has_next_page = GMapsHandler.access_search_next_page(self.DRIVER)
                time.sleep(self.DEFAULT_DELAY)

                # transition logic
                if(has_next_page):
                    STATE = 'COLLECTING_PAGE_RESULTS'
                else:
                    STATE = 'FINISH'

            elif(STATE == 'FINISH'):
                if(self.DEBUG_MODE): print('FINISH')
                # do something for FINISH STATE
                break

            elif(STATE == 'FAIL'):
                if(self.DEBUG_MODE): print('FAIL')
                # do something for FAIL STATE
                break

        BrowserHandler.quit(self.DRIVER)
        return titles

    def get_places(self, search_str):

        STATE = 'CREATING_SESSION'
        PAGE_CURSOR = 0
        PAGE_CURSOR_LIMIT = None
        places = []

        while(True):

            if(STATE == 'CREATING_SESSION'):
    
                # STATE behavior
                if(self.DEBUG_MODE):
                    CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']
                    CHROME_OPTIONS = Options()
                    #CHROME_OPTIONS.add_argument("--user-data-dir=.\chrome-data")
                    CHROME_OPTIONS.add_argument("--enable-automation");
                    self.DRIVER = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=CHROME_OPTIONS)
                else:
                    CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']
                    CHROME_OPTIONS = Options()
                    CHROME_OPTIONS.add_argument('--headless')
                    CHROME_OPTIONS.add_argument('--disable-gpu')  # Last I checked this was necessary.
                    self.DRIVER = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=CHROME_OPTIONS)

                # transition logic
                STATE = 'ACCESSING_GMAPS_URL'

            elif(STATE == 'ACCESSING_GMAPS_URL'):
                if(self.DEBUG_MODE): print(STATE)

                # STATE behavior
                url = GMapsURLAssembler.set_search_str(self.GMAPS_URL, search_str)
                BrowserHandler.set_url(self.DRIVER, url)
                time.sleep(self.DEFAULT_DELAY)

                # transition logic
                url = BrowserHandler.get_url(self.DRIVER)
                if(GMapsHandler.has_title(self.DRIVER)):
                    STATE = 'COLLECTING_SINGLE_RESULT'
                elif(GMapsURLAssembler.is_search_page(url)):
                    STATE = 'COLLECTING_PAGE_RESULTS'
                else:
                    STATE = 'FAIL'

            elif(STATE == 'COLLECTING_PAGE_RESULTS'):
                if(self.DEBUG_MODE): print(STATE)

                # STATE behavior
                GMapsHandler.access_search_page_result_by_index(self.DRIVER, PAGE_CURSOR)
                PAGE_CURSOR_LIMIT = GMapsHandler.get_results_n(self.DRIVER) - 1          
                #print(PAGE_CURSOR_LIMIT)
                #print(PAGE_CURSOR)  
                #print('')  
                time.sleep(self.DEFAULT_DELAY)

                # transition logic
                if(PAGE_CURSOR <= PAGE_CURSOR_LIMIT):
                    STATE = 'COLLECTING_CURSOR_RESULT'
                else:
                    STATE = 'GOING_TO_NEXT_PAGE'

            elif(STATE == 'COLLECTING_CURSOR_RESULT'):
                if(self.DEBUG_MODE): print(STATE)

                # STATE behavior
                url = BrowserHandler.get_url(self.DRIVER)
                place = GMapsHandler.collect_place(self.DRIVER, url, self.CORRECTION_FACTOR)
                places.append(place)
                time.sleep(self.DEFAULT_DELAY)

                if(self.DEBUG_MODE): print(place)
         
                # transition logic
                PAGE_CURSOR += 1
                STATE = 'RETURNING_TO_LIST'

            elif(STATE == 'COLLECTING_SINGLE_RESULT'):
                if(self.DEBUG_MODE): print(STATE)
                
                # STATE behavior
                GMapsHandler.hit_searchbox_button(self.DRIVER)
                time.sleep(self.DEFAULT_DELAY)
                for _ in range(21):
                    GMapsHandler.hit_zoom_in(self.DRIVER)
                time.sleep(self.DEFAULT_DELAY)

                url = BrowserHandler.get_url(self.DRIVER)
                place = GMapsHandler.collect_place(self.DRIVER, url, self.CORRECTION_FACTOR)
                places.append(place)
                if(self.DEBUG_MODE): print(places)

                # transition logic
                STATE = 'FINISH'

            elif(STATE == 'RETURNING_TO_LIST'):
                if(self.DEBUG_MODE): print(STATE)
    
                # STATE behavior
                GMapsHandler.access_search_back_to_results(self.DRIVER)
                time.sleep(self.DEFAULT_DELAY)
                for _ in range(21):
                    GMapsHandler.hit_zoom_in(self.DRIVER)
                time.sleep(self.DEFAULT_DELAY)

                # transition logic
                STATE = 'COLLECTING_PAGE_RESULTS'

            elif(STATE == 'GOING_TO_NEXT_PAGE'):
                if(self.DEBUG_MODE): print(STATE)

                # STATE behavior
                GMapsHandler.access_search_back_to_results(self.DRIVER)
                time.sleep(self.DEFAULT_DELAY)
                has_next_page = GMapsHandler.access_search_next_page(self.DRIVER)
                time.sleep(self.DEFAULT_DELAY)

                # transition logic
                if(has_next_page):
                    STATE = 'COLLECTING_PAGE_RESULTS'
                    PAGE_CURSOR = 1
                else:
                    STATE = 'FINISH'

            elif(STATE == 'FINISH'):
                if(self.DEBUG_MODE): print('FINISH')
                # do something for FINISH STATE
                break

            elif(STATE == 'FAIL'):
                if(self.DEBUG_MODE): print('FAIL')
                # do something for FAIL STATE
                break

        BrowserHandler.quit(self.DRIVER)
        return places

    def get_titles_df():
        pass

    def get_places_df():
        pass