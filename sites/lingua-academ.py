from bs4 import BeautifulSoup
from requests import get
from pprint import pprint

URL = 'https://lingua-academ.ru/blog/380_populyarnih_razgovornih_fraz_na_angliiskom'

def lingua_academ():
    response = get(URL)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    tables_list = soup.find('div', class_='article_body').find_all('tbody')
    themes_list: list[str] = [theme.text.strip() for theme in soup.select('[id^="anchor_"]')]
    phrases: dict[str: dict] = dict()

    for theme, table in zip(themes_list, tables_list):
        theme_phrases: dict[str: str] = dict()

        for tr in table.find_all('tr'):
            p_list = tr.find_all('p')
            theme_phrases[p_list[0].text.strip()] = p_list[1].text.strip()

        phrases[theme] = theme_phrases

    return phrases


pprint(lingua_academ())
