import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Add Caching
CACHE_NAME = 'course_cache.json'
MAX_STALENESS = 1

try:
    CACHE = open(CACHE_NAME, 'r')
    CACHE_DICT = json.loads(CACHE.read())
    CACHE.close()
except:
    CACHE_DICT = {}

def is_stale(cache_entry):
    now = datetime.now().timestamp()
    staleness = now - cache_entry['cache_timestamp']
    return staleness > MAX_STALENESS
    
class CourseListing:
    def __init__(self, course_num, course_name):
        self.num = course_num
        self.name = course_name
    
    def __str__(self):
        return '{}: {}'.format(self.num, self.name)

baseurl = 'https://www.si.umich.edu/programs/courses/catalog'
header = {'User-Agent': 'SI_CLASS'}

try:
    if not is_stale(CACHE_DICT):
        print('Cache found and not stale')
        for course_listing in CACHE_DICT['entries']:
            print(course_listing)
    else:
        raise ValueError('Stale Cache')
except:
    print('No Cache or Stale Cache')
    page_text = requests.get(baseurl, headers=header).text
    page_soup = BeautifulSoup(page_text, 'html.parser')
    # print(page_soup)

    content_div = page_soup.find_all(class_='view-content')
    # print (len(content_div)) # to see if there's more than one

    table_rows = content_div[0].find_all('tr')
    course_listings = []
    for tr in table_rows:
        table_cells = tr.find_all('td')
        if len(table_cells) == 2:
            course_number = table_cells[0].text.strip()
            course_name = table_cells[1].text.strip()
            course_listing = CourseListing(course_number, course_name)
            course_listings.append(course_listing)
    for course_listing in course_listings:
        print(course_listing)

    CACHE_DICT['entries'] = [course_listing.__str__() for course_listing in course_listings]
    CACHE_DICT['cache_timestamp'] = datetime.now().timestamp()
        
    # CACHING
    print('Adding results to Cache...')
    CACHE_WRITE = open(CACHE_NAME, 'w')
    CACHE_WRITE.write(json.dumps(CACHE_DICT))
    CACHE_WRITE.close()
