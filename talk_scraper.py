import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv(override=True)

QUERY_STRING = os.getenv('DPG_QUERY_STRING')
BASE_URL = f'https://www.dpg-verhandlungen.de/year/2024/conference/karlsruhe/search?query={QUERY_STRING}&submit=Suchen'


class DPG_talk:
    def __init__(self):
        self.session_id = None
        self.title = None
        self.authors = []
        self.url = None

    def __str__(self):
        return f'{self.title} by {self.authors}'

    def from_HTML(self, table_row: str):
        self.session_id = table_row.find_all('td', {"class": "scip"})[2].text
        self.title = table_row.find_all('a')[1].text
        self.link = table_row.find_all('a')[1]['href']
        self.authors = [x.text for x in table_row.find_all('span', {"style": "font-variant:small-caps"})]


class HTML_page:
    def __init__(self, URL):
        self.URL = URL
        self.page = requests.get(URL)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.table_body = self.soup.find('tbody')
        self.rows = self.table_body.find_all('tr')

    def has_talks(self):
        return len(self.rows) > 0  

    def get_talks(self):

        talks = []
        for row in self.rows:
            if row.find('a'):
                t = DPG_talk()
                t.from_HTML(row)
                talks.append(t)

        return talks


if __name__ == '__main__':

    talks = []
    page_index = 1

    while True:
        URL = BASE_URL + f'&page={page_index}'

        page = HTML_page(URL)
        if not page.has_talks():
            break

        talks_page = page.get_talks()
        talks.extend(talks_page)

        page_index += 1

    for t in talks:
        print(t)
