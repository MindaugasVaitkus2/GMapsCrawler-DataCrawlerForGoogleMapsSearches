import time
from multiprocessing import Process

from gmapscrawler import GMapsCrawler

def func_1():
    crawler = GMapsCrawler(debug=False, delay=5)
    places = crawler.get_places('estatua da liberdade')
    print('')
    print(places)

def func_2():
    crawler = GMapsCrawler(debug=False, delay=5)
    places = crawler.get_places('hollywood sigh')
    print('')
    print(places)

def func_3():
    crawler = GMapsCrawler(debug=False, delay=5)
    places = crawler.get_places('cristo redentor')
    print('')
    print(places)

def func_4():
    crawler = GMapsCrawler(debug=False, delay=5)
    places = crawler.get_places('muralha da china')
    print('')
    print(places)

def func_5():
    crawler = GMapsCrawler(debug=False, delay=5)
    places = crawler.get_places('torre de toquio')
    print('')
    print(places)    

def func_6():
    crawler = GMapsCrawler(debug=False, delay=5)
    places = crawler.get_places('milwaukee art museum')
    print('')
    print(places)

def func_7():
    crawler = GMapsCrawler(debug=False, delay=5)
    places = crawler.get_places('chicago field museum')
    print('')
    print(places)

def func_8():
    crawler = GMapsCrawler(debug=False, delay=5)
    places = crawler.get_places('petrolina pizzaria recanto pastelaria')
    print('')
    print(places)

def func_9():
    crawler = GMapsCrawler(debug=False, delay=5)
    places = crawler.get_places('seattle century link field')
    print('')
    print(places)


if __name__ == '__main__':

    proc = Process(target=func_1)  
    proc.start()

    proc = Process(target=func_2)  
    proc.start()

    proc = Process(target=func_3)  
    proc.start()

    proc = Process(target=func_4)  
    proc.start()

    proc = Process(target=func_5)  
    proc.start()

    proc = Process(target=func_6)  
    proc.start()

    proc = Process(target=func_7)  
    proc.start()

    proc = Process(target=func_8)  
    proc.start()

    proc = Process(target=func_9)  
    proc.start()


    while(True):
        time.sleep(5)