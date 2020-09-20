
from abc import ABC
import re

class GMapsURL(ABC):

    @staticmethod
    def _get_re_matches(pattern_re, input_str):
        output_matches = []
        for match in re.finditer(pattern_re, input_str):
            output_matches.append(match)
        return output_matches #  .group() .start() .end()

    @staticmethod
    def _get_re_replaced_str(pattern_re, replacement_str, input_str):
        output_str = re.sub(pattern_re, replacement_str, input_str)
        return output_str

    @staticmethod
    def get_cursor(gmaps_url):
        target_str = gmaps_url
        cursor = { 'lat': None, 'lon': None, 'zoom': None }

        pattern_re = '(/@)(-)?[0-9]*[.][0-9]*[,]'
        re_matches = GMapsURL._get_re_matches(pattern_re, target_str)
        cursor['lat'] = float(re_matches[0].group().replace('/@', '').replace(',', ''))

        pattern_re = '[,](-)?[0-9]*[.][0-9]*[,]'
        re_matches = GMapsURL._get_re_matches(pattern_re, target_str)
        cursor['lon'] = float(re_matches[0].group().replace(',', ''))

        pattern_re = '[,][0-9]*[z]'
        re_matches = GMapsURL._get_re_matches(pattern_re, target_str)
        cursor['zoom'] = int(re_matches[0].group().replace(',', '').replace('z', ''))

        return cursor

    @staticmethod
    def set_cursor(gmaps_url, cursor):
        target_str = gmaps_url

        pattern_re = '(/@)(-)?[0-9]*[.][0-9]*[,]'
        replacement_str = '/@' + str(cursor['lat']) + ','
        target_str = GMapsURL._get_re_replaced_str(pattern_re, replacement_str, target_str)

        pattern_re = '[,](-)?[0-9]*[.][0-9]*[,]'
        replacement_str = ',' + str(cursor['lon']) + ','
        target_str = GMapsURL._get_re_replaced_str(pattern_re, replacement_str, target_str)

        pattern_re = '[,][0-9]*[z]'
        replacement_str = ',' +  str(cursor['zoom']) + 'z'
        target_str = GMapsURL._get_re_replaced_str(pattern_re, replacement_str, target_str)

        return target_str

    @staticmethod
    def get_search_str(gmaps_url):
        target_str = gmaps_url
        search_str = None

        pattern_re = '(/maps/search/)(.)*?[/]'
        re_matches = GMapsURL._get_re_matches(pattern_re, target_str)
        search_str = re_matches[0].group().replace('/maps/search/', '').replace('/', '').replace('+', ' ')
        return search_str

    @staticmethod
    def set_search_str(gmaps_url, search_str):
        target_str = gmaps_url
        search_str = search_str.replace(' ', '+')
        
        if('/search/' in target_str):
            pattern_re = '(/maps/search/)(.)*?[/]'
            replacement_str = '/maps/search/' + str(search_str) + '/'
            target_str = GMapsURL._get_re_replaced_str(pattern_re, replacement_str, target_str)
        else:
            pattern_re = '(/maps/)(.)*'
            replacement_str = '/maps/search/' + str(search_str) + '/'
            target_str = GMapsURL._get_re_replaced_str(pattern_re, replacement_str, target_str)
        return target_str

if __name__ == '__main__':

    GMAPS_URL = 'https://www.google.com.br/maps/search/New+York+pizza+place/@40.7110686,-73.9962479,12z/data=!3m1!4b1'
    new_cursor = { 'lat': -20.256, 'lon': 10.0, 'zoom': 17 }
    new_search_str = 'Chicago pizza place'

    print('')
    print('ORIGINAL URL:      ', GMAPS_URL)
    print('NEW CURSOR:        ', new_cursor)
    print('NEW SEARCH STRING: ', new_search_str)
    print('')
    print('ORIGINAL CURSOR IS:              ', GMapsURL.get_cursor(GMAPS_URL))
    print('WITH NEW CURSOR, THE NEW URL IS: ', GMapsURL.set_cursor(GMAPS_URL, new_cursor))
    print('')
    print('ORIGINAL SEARCH STRING IS:              ', GMapsURL.get_search_str(GMAPS_URL))
    print('WITH NEW SEARCH STRING, THE NEW URL IS: ', GMapsURL.set_search_str(GMAPS_URL, new_search_str))
    print('')