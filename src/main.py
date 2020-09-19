
import time

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_re_matches(pattern_re, input_str):
    output_matches = []
    for match in re.finditer(pattern_re, input_str):
        output_matches.append(match)
    return output_matches #  .group() .start() .end()

def get_re_replaced_str(pattern_re, replacement_str, input_str):
    output_str = re.sub(pattern_re, replacement_str, input_str)
    return output_str



def get_current_url():
    return driver.current_url

def set_current_url(url_str):
    driver.get(url_str)

def get_gmaps_url(lat, lon, zoom):
    cursor_str = '@' + str(lat) + ',' + str(lon) + ',' + str(zoom) + 'z'
    gmaps_search_str = 'https://www.google.com/maps/' + cursor_str
    return gmaps_search_str

def get_gmaps_search_url(search_str, lat, lon, zoom):
    search_str = search_str.replace(' ', '+')
    cursor_str = '@' + str(lat) + ',' + str(lon) + ',' + str(zoom) + 'z'
    gmaps_search_str = 'https://www.google.com/maps/search/' + search_str + '/' + cursor_str
    return gmaps_search_str

def get_gmaps_search_page_itens():
    search_page_itens = driver.find_elements_by_class_name("section-result-title")
    return search_page_itens

def goto_gmaps_search_next_page():
    possible_enabled_target_elements = driver.find_elements_by_id('n7lv7yjyC35__section-pagination-button-next')
    try:
        possible_enabled_target_elements[0].click()
        return True
    except exceptions.ElementClickInterceptedException:
        return False
    except exceptions.ElementNotInteractableException:
        return False
    except exceptions.StaleElementReferenceException:
        return False


#list_search_str
#item_search_str



url_inicial = "https://www.google.com/maps" #/@-8.5112613,-39.3102358,15z
PATH = r'C:\Users\smurilogs\Desktop\gmaps-crawler\src\chromedriver.exe'

chrome_options = webdriver.ChromeOptions() #Options()
chrome_options.add_argument("--user-data-dir=.\chrome-data")
chrome_options.add_argument("--enable-automation")
#chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
#chrome_options.add_argument("--start-maximized")

#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(executable_path=PATH, options=chrome_options)

driver.get('https://www.google.com.br/maps/search/petrolina+pizzaria/')

time.sleep(2)
search_itens_texts = []
page_itens = []
has_next_page = True
while(has_next_page):
    time.sleep(2)
    page_itens = get_gmaps_search_page_itens()
    for page_item in page_itens:
        search_itens_texts.append(page_item.text)
    has_next_page = goto_gmaps_search_next_page()

target_text = search_itens_texts[0]

time.sleep(2)
driver.get('https://www.google.com.br/maps/search/petrolina+pizzaria/')

time.sleep(2)
has_target_found = False
has_next_page = True
while(has_next_page):
    time.sleep(2)
    page_itens = get_gmaps_search_page_itens()
    for page_item in page_itens:
        print(page_item.text)
        print(target_text)
        print(page_item.text == target_text)
        print(' ')
        if(page_item.text == target_text):
            has_target_found = True
            has_next_page = False    
            time.sleep(2)            
            #driver.get('https://www.google.com.br/maps/search/petrolina+pizzaria//@0.0,0.0,21z/')
            #time.sleep(2) 
            page_item.click()
            time.sleep(2)
            break
    if(not has_target_found):
        has_next_page = goto_gmaps_search_next_page()

time.sleep(10)


#for item_text in search_itens_texts:
#    print(item_text)

#set_current_url(get_gmaps_url(0.0, 0.0, 21))
#time.sleep(2)
#set_current_url(get_gmaps_search_url('petrolina pizzaria ' + search_itens_texts[0], 0.0, 0.0, 21))
#time.sleep(10)


#time.sleep(10)
#elements = driver.find_elements_by_class_name("section-result-title") 
#print(len(elements))

#time.sleep(2)
#elements[0].click()
#print(driver.current_url)

driver.quit()


#print(get_gmaps_search_url('petrolina pizzaria'))

#

#driver.get(url_inicial)
#caixa_texto = driver.find_element_by_id("searchboxinput")
#caixa_texto.send_keys("rua do dende petrolina")

