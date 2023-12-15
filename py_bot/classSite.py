import requests
from bs4 import BeautifulSoup as b
import time
from datetime import datetime


class Site:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.total_list = []
        self.info = [('FILM', 'URL', datetime.now())]

    def __parse(self):
        r = requests.get(self.url, headers=self.headers)
        time.sleep(3)
        return b(r.text, 'html.parser')

    def get_total_list(self):
        soup = self.__parse()
        for films in soup.find_all('div', class_='shortpost'):
            link = films.div.a['href']
            name = films.div.a.img['title']
            tmp = [name, link]
            self.info.append(tmp)
            self.total_list.append(f'{name} {link}')
        return self.total_list

    def get_info(self):
        return self.info


url = 'https://www.baskino.re/'
headers = {
    'Accept': '*/*',
    'User_Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.731 Mobile Safari/537.36'
}
s = Site(url, headers)
if __name__ == '__main__':
    print('This is a parser')
