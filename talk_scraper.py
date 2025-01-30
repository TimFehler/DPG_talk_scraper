import requests
from bs4 import BeautifulSoup
import yaml


class DPG_talk:
    def __init__(self):
        self.session_id = None
        self.title = None
        self.authors = []
        self.presenting_author = None
        self.link = None

    def __str__(self):
        return f'({self.session_id}): {self.title} by {self.presenting_author}'

    def from_HTML(self, table_row: str):
        self.session_id = table_row.find_all('td', {"class": "scip"})[2].text
        self.title = table_row.find_all('a')[1].text
        self.link = table_row.find_all('a')[1]['href']
        self.authors = [x.text for x in table_row.find_all('span', {"style": "font-variant:small-caps"})]
        
        # Identify presenting author
        bullet = table_row.find(string=lambda text: text and "\u2022" in text)

        if bullet:
            self.presenting_author = bullet.find_next('span').text

    def to_dict(self):
        """Convert object to dictionary for YAML serialization."""
        return {
            'session_id': self.session_id,
            'title': self.title,
            'authors': self.authors,
            'presenting_author': self.presenting_author,
            'link': self.link
        }

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

    talks_dict = [t.to_dict() for t in talks]

    # Write to YAML file

    output_file = config['DPG24']['output_file']
    with open(f'{output_file}', 'w') as file:
        yaml.dump(talks_dict, file, allow_unicode=True, default_flow_style=False)

    print(f'Wrote talks to {output_file}')
