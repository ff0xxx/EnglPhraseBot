from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from parsers import skyeng

# -------------------------select_site_keyboard-------------------------

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

# -------------------------skyeng_inline_keyboard-------------------------

btn0 = InlineKeyboardButton(text='link',
                            url=skyeng.URL)
btns = [InlineKeyboardButton(text=theme, callback_data='skyeng') for theme in skyeng.themes_list]

builder = InlineKeyboardBuilder().row(*btns, width=1).add(btn0)

skyeng_inline_keyboard = builder.as_markup()
