import re

def get_re_matches(pattern_re, input_str):
    output_matches = []
    for match in re.finditer(pattern_re, input_str):
        output_matches.append(match)
    return output_matches #  .group() .start() .end()

def get_re_replaced_str(pattern_re, replacement_str, input_str):
    output_str = re.sub(pattern_re, replacement_str, input_str)
    return output_str

def get_gmaps_url_cursor(gmaps_url):
    target_str = gmaps_url
    cursor = { 'lon': None, 'lat': None, 'zoom': None }

    pattern_re = '(/@)(-)?[0-9]*[.][0-9]*[,]'
    re_matches = get_re_matches(pattern_re, target_str)
    cursor['lon'] = float(re_matches[0].group().replace('/@', '').replace(',', ''))

    pattern_re = '[,](-)?[0-9]*[.][0-9]*[,]'
    re_matches = get_re_matches(pattern_re, target_str)
    cursor['lat'] = float(re_matches[0].group().replace(',', ''))

    pattern_re = '[,][0-9]*[z]'
    re_matches = get_re_matches(pattern_re, target_str)
    cursor['zoom'] = int(re_matches[0].group().replace(',', '').replace('z', ''))

    return cursor

def set_gmaps_url_cursor(gmaps_url, cursor):
    target_str = gmaps_url

    pattern_re = '(/@)(-)?[0-9]*[.][0-9]*[,]'
    replacement_str = '/@' + str(cursor['lon']) + ','
    target_str = get_re_replaced_str(pattern_re, replacement_str, target_str)

    pattern_re = '[,](-)?[0-9]*[.][0-9]*[,]'
    replacement_str = ',' + str(cursor['lat']) + ','
    target_str = get_re_replaced_str(pattern_re, replacement_str, target_str)

    pattern_re = '[,][0-9]*[z]'
    replacement_str = ',' +  str(cursor['zoom']) + 'z'
    target_str = get_re_replaced_str(pattern_re, replacement_str, target_str)

    return target_str

def get_gmaps_url_search_str(gmaps_url):
    target_str = gmaps_url
    search_str = None

    pattern_re = '(/maps/search/)(.)*?[/]'
    re_matches = get_re_matches(pattern_re, target_str)
    search_str = re_matches[0].group().replace('/maps/search/', '').replace('/', '').replace('+', ' ')
    return search_str

def set_gmaps_url_search_str(gmaps_url, search_str):
    target_str = gmaps_url
    search_str = search_str.replace(' ', '+')
    
    if('/search/' in target_str):
        pattern_re = '(/maps/search/)(.)*?[/]'
        replacement_str = '/maps/search/' + str(search_str) + '/'
        target_str = get_re_replaced_str(pattern_re, replacement_str, target_str)
    else:
        pattern_re = '(/maps/)(.)*'
        replacement_str = '/maps/search/' + str(search_str) + '/'
        target_str = get_re_replaced_str(pattern_re, replacement_str, target_str)
    return target_str