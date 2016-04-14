# -*- coding: utf-8 -*-

import MeCab

from google import search
from bs4 import BeautifulSoup
import urllib

from image.functions import has_image

def find_appropriate_news(text):
    nouns = get_nouns(text)
    if not nouns:
        return None
    else:
        query = get_query(nouns)
        return get_news(query)

def get_nouns(text):
    nouns = []
    mt = MeCab.Tagger("mecabrc")
    encoded_text = text.encode('utf-8')
    res = mt.parseToNode(encoded_text)

    while res:
        print res.surface
        arr = res.feature.split(",")
        if arr[0] == '名詞':
            decoded_text = res.surface.decode('utf-8')
            nouns.append(decoded_text)
        res = res.next
    print nouns
    return nouns


def get_query(nouns):
    keywords = u' '.join(nouns)
    site = u'site:newspicks.com'
    return u' '.join([keywords, site])


def get_news(query):
    for url in search(query.encode('utf-8'), stop=10, lang="en"):
        print url
        soup = BeautifulSoup(urllib.urlopen(url))
        title = soup.find("title").text
        picker = soup.find('div', class_="name").text if soup.find('div', class_="name") else None
        news_id = get_news_id(url)
        if news_id and has_image(news_id):
            return  {
                'url': url,
                'title': title,
                'picker': picker,
                'news_id': news_id,
            }
    return None


def get_news_id(url):
    tokens = url.split('/')
    for token in tokens:
        if token.isdigit():
            return token
    return None
