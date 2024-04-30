from requests   import get
from time       import time, sleep

BOT_TOKEN = '7079074797:AAFU_V0jeIARYquvZE36zwCRmbnG6VZ_FZM'
API_URL = 'https://api.telegram.org/bot'
timeout = 40

offset = -2
chat_id: int


while True:
    updates = get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']

            match result['message']['text'].lower():
                case 'привет':
                    TEXT = 'Ну здравствуй, ' + result['message']['from']['first_name']
                case 'пока':
                    TEXT = 'Всё только впереди >:)'
                case _:
                    TEXT = 'Серкан Болат поцелуй меня'

            get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')

    sleep(1)
