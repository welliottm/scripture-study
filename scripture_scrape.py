import logging
import re

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

bom_books = {
             # '1-ne':22,
             # '2-ne':33,
             # 'jacob':7,
             # 'enos':1,
             # 'jarom':1,
             # 'omni':1,
             # 'w-of-m':1,
             # 'mosiah':29,
             # 'alma':63,
             # 'hel':16,
             # '3-ne':30,
             '4-ne':1,
             # 'morm':9,
             # 'ether':15,
             # 'moro':10,
}

def get_chapter_response(library, book, chapter_num):
    logging.debug(f'Retreiving content for chapter {chapter_num}')
    url = ('https://www.churchofjesuschrist.org/study/scriptures/'
           + library
           + '/'
           + book
           + '/'
           + chapter_num
           + '?lang=eng')
    response = requests.get(url)
    logging.debug(f'Received HTTP status code: {response.status_code}')
    soup = BeautifulSoup(response.content, features='lxml')
    body = soup.find('div', {'class': 'body-block'})
    # Add a space after each Verse
    for verse in body.find_all('p'):
        verse.insert_after(' ')
    # Remove all superscript markers used for footnotes
    for sup in body('sup'):
        sup.decompose()
    # Remove Verse numbers
    for sup in body('span'):
        sup.decompose()
    return body

def get_chapter_content(library, book_dict):
    content_dict = {}
    for book in book_dict:
        logging.debug(f'Starting iteration for book:{book} in library:{library}')
        for chapter_num in range(1, (book_dict[book] + 1)):
            response = get_chapter_response(library, book, str(chapter_num))
            logging.debug('Adding response content to content_dict')
            content_dict.update({(book + '--ch' + str(chapter_num)):response.text})
    return content_dict

if __name__=='__main__':
    chapter_content = get_chapter_content('bofm', bom_books)
    print(chapter_content)
    # with open('test_output.txt', mode='wt', encoding='utf-8') as file:
    #     file.write(chapter_content['4-ne--ch1'])
