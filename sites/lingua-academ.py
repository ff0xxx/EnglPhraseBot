from bs4 import BeautifulSoup
from requests import get
from pprint import pprint

URL = 'https://lingua-academ.ru/blog/380_populyarnih_razgovornih_fraz_na_angliiskom'

def lingua_academ():
    response = get(URL)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text)

    res_dict = dict()

    tables_list = soup.find('div', class_='article_body').find_all('tbody')

    for table in tables_list:
        tr_list = table.find_all('tr')

        for tr in tr_list[:-2]:
            td_list = tr.find_all('td')

            res_dict[td_list[0].text.strip()] = td_list[1].text.strip()

    return res_dict


# pprint(lingua_academ()) - обрабатывается почему-то не вся страница
