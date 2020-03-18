import logging
import re

from requests_html import HTMLSession

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
             'morm':9,
             # 'ether':15,
             # 'moro':10,
}

def get_chapter_response(library, book, chapter_num):
    session = HTMLSession()
    url = ('https://www.churchofjesuschrist.org/study/scriptures/'
           + library
           + '/'
           + book
           + '/'
           + chapter_num
           + '?lang=eng')
    chapter_response = session.get(url)
    return chapter_response

def get_chapter_content(library, book_dict):
    content_dict = {}
    for book in book_dict:
        logging.debug(f'Iterating over {book}')
        for chapter_num in range(1, (book_dict[book] + 1)):
            logging.debug(f'Retreiving content for chapter {chapter_num}')
            response = get_chapter_response(library, book, str(chapter_num))
            logging.debug(f'Received status code {response.status_code}')
            logging.debug('Retreived response')
            content_dict.update({(book+str(chapter_num)):response.content})
            logging.debug('Adding response content to content_dict')
    return content_dict

if __name__=='__main__':
    chapter_content = get_chapter_content('bofm', bom_books)
    print(chapter_content['morm2'])
