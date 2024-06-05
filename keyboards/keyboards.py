from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.filters.callback_data import CallbackData
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

btns = [InlineKeyboardButton(text=theme, callback_data=str(i)) for i, theme in enumerate(skyeng.themes_list)]
btn0 = InlineKeyboardButton(text='link',
                            url=skyeng.URL)

builder = InlineKeyboardBuilder().row(*btns, width=1).add(btn0)
skyeng_inline_keyboard = builder.as_markup()

# -------------------------skyeng_callback_keyboard-------------------------


class PhrasesCallbackFactory(CallbackData, prefix='phrase'):
    site_id: int
    theme_id: int
    phrase_id: int
    lang_id: int


def theme_keyboard(theme_index: str) -> InlineKeyboardMarkup:
    print('THEME (получаю): ------------>', theme_index)

    theme = list(skyeng.phrases.keys())[int(theme_index)]

    phr = []
    for i, eng in enumerate(skyeng.phrases[theme]):
        phr.append(InlineKeyboardButton(text=eng,
                                        callback_data=PhrasesCallbackFactory(site_id=0,
                                                                             theme_id=int(theme_index),
                                                                             phrase_id=i,
                                                                             lang_id=0).pack()))

    keyboard_builder = InlineKeyboardBuilder().row(*phr, width=1)

    return keyboard_builder.as_markup()


# -------------------------skyeng_callback_keyboard-------------------------

def phrase_keyboard(callback_data: str):
    print('THEME 2 (получаю): ------------>', callback_data)

    # site:theme:phrase:lang <-- передаю параметры определенной КНОПКИ
    callback = list(map(int, callback_data.split(':')[1:]))
    print(callback)

    theme = list(skyeng.phrases.keys())[int(callback[1])]
    print('THEME: ', theme)

    phr = []
    for i, eng in enumerate(skyeng.phrases[theme]):
        phr.append(InlineKeyboardButton(text=eng,
                                        callback_data=PhrasesCallbackFactory(site_id=0,
                                                                             theme_id=callback[1],
                                                                             phrase_id=i,
                                                                             lang_id=0).pack()))

    # "переворачиваю" карточку, нажав на которую пришел апдейт с этим callback_data
    eng = phr[callback[2]]
    print('ENG:', eng.text)
    phr[callback[2]] = InlineKeyboardButton(text=skyeng.phrases[theme][eng.text],
                                            callback_data=PhrasesCallbackFactory(site_id=0,
                                                                                 theme_id=callback[1],
                                                                                 phrase_id=callback[2],
                                                                                 lang_id=(callback[3]+1)%2).pack())

    keyboard_builder = InlineKeyboardBuilder().row(*phr, width=1)

    return keyboard_builder.as_markup()