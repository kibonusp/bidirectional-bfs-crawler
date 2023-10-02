from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse
import re

origin = 'https://en.wikipedia.org/wiki/Cheese'
destination = 'Culture of Europe'

def formatURL(url):
    if url[0] == '/':
        url = 'https://en.wikipedia.org' + url
    
    return url

class Page:
    def __init__(self, url):
        self.url = formatURL(url)
        self.getPage(self.url)
    
    def getPage(self, url):
        try:
            html = urlopen(url)
            bs = BeautifulSoup(html, 'html.parser')
            self.bs = bs
        except:
            self.bs = None

    def getTitle(self):
        if self.bs is None:
            return None
        title = self.bs.select('.mw-page-title-main')[0].get_text()
        return title

    def getNeighbors(self):
        regex = '\/wiki\/(?!(.*:)).*'
        return set([formatURL(link.attrs["href"]) for link in self.bs.find_all('a', {'href': re.compile(regex)})])
        
cheese_page = Page(origin)
print(cheese_page.getTitle())
print(cheese_page.getNeighbors())