
from abc import ABC

from gmapsurlassembler import GMapsURLAssembler

class GMapsHandler(ABC):

    @staticmethod
    def get_results_n(DRIVER):
        elements_found = DRIVER.find_elements_by_class_name("section-result-title")
        return len(elements_found)

    @staticmethod
    def collect_search_page_results(DRIVER):
        elements_found = DRIVER.find_elements_by_class_name("section-result-title")
        search_page_results = []
        for element in elements_found:
            search_page_results.append({ 'title': element.text })
        return search_page_results

    @staticmethod
    def collect_title(DRIVER):
        elements_found = DRIVER.find_elements_by_class_name("section-hero-header-title-title")
        texts_found = []
        for element in elements_found:
            texts_found.append({'value': element.text})
        if(len(texts_found) > 0):
            return texts_found[0]
        else:
            return {'value': None }

    @staticmethod
    def collect_labels(DRIVER):
        elements_found = DRIVER.find_elements_by_class_name("ugiz4pqJLAG__primary-text")
        texts_found = []
        for element in elements_found:
            texts_found.append({'value': element.text})
        if(len(texts_found) > 0).:
            return texts_found
        else:
            return [{'value': None }]

    @staticmethod
    def collect_coordinates(url, CORRECTION_FACTOR):
        coordinates = {
            "latitude": GMapsURLAssembler.get_cursor(url)['lat'],
            "longitude": GMapsURLAssembler.get_cursor(url)['lon'] + CORRECTION_FACTOR
        }
        return coordinates

    @staticmethod
    def collect_place(DRIVER, url, CORRECTION_FACTOR):
        place = {
            "place": { 
                "title": GMapsHandler.collect_title(DRIVER)['value'],
                "coordinates": GMapsHandler.collect_coordinates(url, CORRECTION_FACTOR),
                "labels": GMapsHandler.collect_labels(DRIVER)
            }
        }
        return place

    @staticmethod
    def access_search_page_result_by_index(DRIVER, index):
        possible_enabled_target_elements = DRIVER.find_elements_by_class_name('section-result-text-content')
        try:
            possible_enabled_target_elements[index].click()
            return True
        except Exception as e:
            #print(e)
            return False

    @staticmethod
    def access_search_next_page(DRIVER):
        possible_enabled_target_elements = DRIVER.find_elements_by_id('n7lv7yjyC35__section-pagination-button-next')
        try:
            possible_enabled_target_elements[0].click()
            return True
        except Exception as e:
            #print(e)
            return False

    @staticmethod
    def access_search_back_to_results(DRIVER):
        possible_enabled_target_elements = DRIVER.find_elements_by_class_name('section-back-to-list-button')
        try:
            possible_enabled_target_elements[0].click()
            return True
        except Exception as e:
            #print(e)
            return False

    @staticmethod
    def hit_zoom_in(DRIVER):
        possible_enabled_target_elements = DRIVER.find_elements_by_id('widget-zoom-in')
        try:
            possible_enabled_target_elements[0].click()
            return True
        except Exception as e:
            #print(e)
            return False        

    @staticmethod
    def hit_zoom_out(DRIVER):
        possible_enabled_target_elements = DRIVER.find_elements_by_id('widget-zoom-out')
        try:
            possible_enabled_target_elements[0].click()
            return True
        except Exception as e:
            #print(e)
            return False   

    @staticmethod
    def hit_searchbox_button(DRIVER):
        possible_enabled_target_elements = DRIVER.find_elements_by_id('searchbox-searchbutton')
        try:
            possible_enabled_target_elements[0].click()
            return True
        except Exception as e:
            #print(e)
            return False   

    @staticmethod
    def has_title(DRIVER):
        elements_found = DRIVER.find_elements_by_class_name("section-hero-header-title-title")
        if(len(elements_found) > 0):
            return True
        else:
            return False