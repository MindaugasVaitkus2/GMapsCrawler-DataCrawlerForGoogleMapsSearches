
def get_current_url(driver):
    return driver.current_url

def set_current_url(driver, url_str):
    driver.get(url_str)