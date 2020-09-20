
from abc import ABC

class Browser(ABC):

    @staticmethod
    def get_url(driver):
        return driver.current_url
    
    @staticmethod
    def set_url(driver, url_str):
        driver.get(url_str)