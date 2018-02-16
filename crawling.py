import requests
from bs4 import BeautifulSoup
import json

baseurl = 'https://www.si.umich.edu/programs/courses/catalog'
header = {'User-Agent': 'SI_CLASS'}

page_text = requests.get(baseurl, headers=header).text
page_soup = BeautifulSoup(page_text, 'html.parser')
# print(page_soup)

content_div = page_soup.find_all(class_='view-content')
# print (len(content_div)) # to see if there's more than one

class CourseListing:
    def __init__(self, course_num, course_name):
        self.num = course_num
        self.name = course_name
    
    def __str__(self):
        return '{}: {}'.format(self.num, self.name)

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