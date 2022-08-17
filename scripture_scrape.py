import csv
import json
import logging
import re
import requests
from bs4 import BeautifulSoup
from collections import Counter

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

logging.basicConfig(level=logging.DEBUG)


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
    # Remove span garbage
    span_to_remove = ['verse-number','clarity-word','para-mark']
    for element in span_to_remove:
        for item in body.find_all('span', {'class', element}):
            item.decompose()
    # Remove sup garbage
    sup_to_remove = ['marker']
    for element in sup_to_remove:
        for item in body.find_all('sup', {'class', element}):
            item.decompose()
    # Add a space after each Verse
    for verse in body.find_all('p'):
        verse.insert_after(' ')
    return body

def get_chapter_content():
    with open('books_chapters.csv') as csv_file:
        books_chapters = csv.DictReader(csv_file)
        content_dict = {}
        for line in books_chapters:
            logging.debug(f"Starting iteration for book:{line['book']} in library:{line['library']}")
            for chapter_num in range(1, (int(line['total_chapters']) + 1)):
                response = get_chapter_response(library=line['library'], book=line['book'], chapter_num=str(chapter_num))
                logging.debug('Adding response content to content_dict')
                content_dict.update({(line['book'] + '--ch' + str(chapter_num)):response.text})
        return content_dict

def combine_text(dictionary):
    '''Combines all dictionary values into one string. This concatenates all scripture
    content into one string of text without chapter numbers or verse numbers.
    '''
    logging.debug('Combining text into one string')
    text_dict_values = dictionary.values()
    text_dict_values = ''.join(text_dict_values)
    return text_dict_values

def tokenize(text_string, min_word_length):
    '''Take the scripture string and return a list of tokens.
    '''
    tokens = word_tokenize(text_string)
    # Define stopwords, and add custom words
    scripture_stopwords = stopwords.words('english')
    extra_words = ['also', 'came', 'come', 'said', 'say', 'thou', 'thus', 'thy', 'unto', 'yea']
    scripture_stopwords.extend(extra_words)
    # Select words that meet the following criteria:
    # (1) Word is alphabetic
    # (2) Word length is >= {min_word_length}
    # (3) Word is not found in the "stopwords" list
    tokens = [word for word in tokens if word.isalpha()
                                      and len(word) >= min_word_length
                                      and word.lower() not in scripture_stopwords]
    return tokens

def count_words(word_list):
    word_counter = Counter(word_list)
    return word_counter

if __name__=='__main__':
    chapter_content = get_chapter_content()
    combined_text = combine_text(dictionary=chapter_content)
    with open('text_output.txt', mode='wt', encoding='utf-8') as file:
        file.write(combined_text)
    tokens = tokenize(text_string=combined_text, min_word_length=3)
    word_count = count_words(word_list=tokens)
    print(word_count)
