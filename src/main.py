from gmapscrawler import GMapsCrawler

if __name__ == '__main__':

    # GMapsCrawler instatiation
    crawler = GMapsCrawler(debug=True)

    # example of a search string
    search_str = 'pizzaria petrolina'

    # uses search string to get a list titles
    #titles = crawler.get_titles(search_str)
    #print(titles)

    # uses search string to get a list of detailed places
    places = crawler.get_places(search_str)
    print(places)