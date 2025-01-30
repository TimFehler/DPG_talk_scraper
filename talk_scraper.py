import requests
from bs4 import BeautifulSoup
import yaml


class DPG_talk:
    def __init__(self):
        self.session_id = None
        self.title = None
        self.authors = []
        self.link = None

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
    with open('config.yml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    query_strings = config['DPG24']['query_strings']

    talks = []
    for query_string in query_strings:
        # Construct query URL
        base_url = config['DPG24']['url'] + f"?query={query_string}&submit=Suchen"
        page_index = 1

        while True:
            url = base_url + f'&page={page_index}'

            page = HTML_page(url)
            if not page.has_talks():
                break
            
            print('Getting talks from', url)

            talks_page = page.get_talks()
            talks.extend(talks_page)

            page_index += 1

    # Remove duplicates (check URL for that)
    talks = list({t.link: t for t in talks}.values())

    print(f'Found {len(talks)} unique talks')

    for t in talks:
        print(t)
