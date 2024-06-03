from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


button_1 = KeyboardButton(text='skyeng (100)')
button_2 = KeyboardButton(text='smileenglish (200)')
button_3 = KeyboardButton(text='lingua-academ (380)')

select_site_keyboard = ReplyKeyboardMarkup(
    keyboard=[[button_1],
              [button_2],
              [button_3]],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Кнопки нажимай, дубина')


btn1 = KeyboardButton(text='Hello')
btn2 = KeyboardButton(text='Goodbye!')
btn3 = KeyboardButton(text='How are you?')

skyeng_keyboard = ReplyKeyboardMarkup(
    keyboard=[[btn1, btn2],
              [btn3]],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Надо выбрать тему для 100 фраз')