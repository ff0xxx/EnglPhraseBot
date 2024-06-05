from bs4 import BeautifulSoup
from requests import get

URL = 'https://skyeng.ru/articles/100-poleznyh-razgovornyh-fraz-na-anglijskom/'

response = get(URL)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

themes_list = [theme.text.strip(':') for theme in soup.select('div[class="-adults root"] > h2, '
                                                              'div[class="-adults root"] > h3')[:-1]]
tables_list = soup.find_all('tbody')
phrases: dict[str: dict] = dict()

for theme, table in zip(themes_list, tables_list):
    theme_phrases = dict()

    for tr in table.find_all('tr'):
        td_list = tr.find_all('td')
        eng = td_list[0].text.strip()
        rus = td_list[1].text.strip()
        theme_phrases[eng] = rus

    phrases[theme] = theme_phrases
