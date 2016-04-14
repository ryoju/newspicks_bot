# -*- coding: utf-8 -*-

from google import search
from bs4 import BeautifulSoup
import urllib

for url in search("クック パッド 内紛 site:newspicks.com", stop=10, lang="en"):
    soup = BeautifulSoup(urllib.urlopen(url))
    print url
    print soup.find("title").text
