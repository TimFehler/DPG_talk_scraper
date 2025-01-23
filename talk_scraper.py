import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

QUERY_STRING = os.getenv('QUERY_STRING')

URL = f'https://www.dpg-verhandlungen.de/year/2024/conference/karlsruhe/search?query={QUERY_STRING}&submit=Suchen'

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find_all('td', class_='scip')

print(results)