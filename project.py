from bs4 import BeautifulSoup
import string
import random
import json
import urllib3
from urllib3 import poolmanager

class propigator:
    HOME_ADDRESS = 'https://www.google.com/search?q={}'
    URL_ADDRESS = 'https://www.google.com'

    def start_prop(self):
        self.props = {}
        self.urls = []
        try:
            self.visited = self.read_visited()
        except FileNotFoundError:
            self.visited = []
            self.write_visited()
        self.http = poolmanager.PoolManager()
        self.learn()

    def learn(self):
        char = random.choice(string.ascii_letters)
        print(char)
        content = self.http.request('GET', self.HOME_ADDRESS.format(char))
        soup = BeautifulSoup(content.data)
        for url in soup.find_all('a', href=True):
            if url['href'] not in self.visited:
                print(url['href'])
                self.urls.append(url['href'])
        self.visit_urls()

    def visit_urls(self):
        for url in self.urls:
            try:
                if url[0:4] == 'http' and url not in self.visited:
                    content = self.http.request('GET', url)
                    soup = BeautifulSoup(content.data)
                    for urls in soup.find_all('a', href=True):
                        if urls['href'] not in self.visited:
                            print(urls['href'])
                            self.urls.append(urls['href'])
                elif url not in self.visited:
                    content = self.http.request('GET', self.URL_ADDRESS.format(url))
                    soup = BeautifulSoup(content.data)
                    for urls in soup.find_all('a', href=True):
                        if urls['href'] not in self.visited:
                            print(urls['href'])
                            self.urls.append(urls['href'])
                self.visited.append(url)
                self.write_visited()
            except urllib3.exceptions.MaxRetryError:
                self.learn()



    def read_visited(self):
        with open('visited.json','r') as r:
            return json.load(r)

    def write_visited(self):
        with open('visited.json', 'w') as w:
            json.dump(self.visited, w)

x = propigator().start_prop()
