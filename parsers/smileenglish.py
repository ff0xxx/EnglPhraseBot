from bs4        import BeautifulSoup
from requests   import get

URL = 'https://smileenglish.ru/technique/anglijskij-dlya-turistov-200-fraz/'

response = get(URL)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

themes_list: list[str] = [theme.text.strip() for theme in soup.select('h2 > strong')[1:] if theme.text.strip()]
tables_list = soup.find_all('tbody')
phrases: dict[str: dict] = dict()

for theme, table in zip(themes_list, tables_list):
    theme_phrases: dict[str: str] = dict()

    for tr in table.find_all('tr')[1:]:
        p_list = tr.find_all('p')
        eng = p_list[1].text.strip()
        rus = p_list[0].text.strip()
        theme_phrases[eng] = rus

    phrases[theme] = theme_phrases
