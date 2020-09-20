
from abc import ABC

class Browser(ABC):

    @staticmethod
    def get_url(DRIVER):
        return DRIVER.current_url
    
    @staticmethod
    def set_url(DRIVER, url_str):
        DRIVER.get(url_str)

    @staticmethod
    def close(DRIVER):
        DRIVER.quit()
