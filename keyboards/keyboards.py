from aiogram.types                  import (KeyboardButton, ReplyKeyboardMarkup,
                                            InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
from aiogram.filters.callback_data  import CallbackData
from aiogram.utils.keyboard         import InlineKeyboardBuilder
from parsers                        import skyeng, smileenglish, lingua_academ
from lexicon.lexicon_ru             import LEXICON_RU


sites_name_module = {
    'skyeng': skyeng,
    'smileenglish': smileenglish,
    'lingua-academ': lingua_academ
}

sites_name_index = {
    'skyeng': 0,
    'smileenglish': 1,
    'lingua-academ': 2
}

sites_index_module = {
    0: skyeng,
    1: smileenglish,
    2: lingua_academ
}


# site +
def site_keyboard() -> ReplyKeyboardMarkup:
    """ДЕЛАЮ ОБЫЧНУЮ КЛАВИАТУРУ ДЛЯ ВЫБОРА САЙТА"""
    button_1 = KeyboardButton(text='skyeng (100)')
    button_2 = KeyboardButton(text='smileenglish (200)')
    button_3 = KeyboardButton(text='lingua-academ (380)')

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1],
                  [button_2],
                  [button_3]],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Кнопки нажимай, лапочка')

    return keyboard


# site +
def theme_keyboard(site_name: str) -> InlineKeyboardMarkup:
    """ДЕЛАЮ INLINE-КЛАВИАТУРУ ДЛЯ ТЕМ ПО САЙТУ"""

    site_index: int = sites_name_index[site_name]
    btns = [InlineKeyboardButton(text=theme, callback_data=f'{theme_index} {site_index}')
            for theme_index, theme in enumerate(sites_name_module[site_name].themes_list)]

    btn0 = InlineKeyboardButton(text='link',
                                url=sites_name_module[site_name].URL)

    builder = InlineKeyboardBuilder().row(*btns, width=1).add(btn0)

    return builder.as_markup()


# site +
def pagination_add_func(btn_list: list[InlineKeyboardButton]) -> InlineKeyboardMarkup:
    """ИЗ СПИСКА INLINE-КНОПОК ДЕЛАЮ PAGINATION-КЛАВИАТУРУ"""
    print('BTN_LIST: ', btn_list)
    # site:theme:phrase:lang:page
    first_btn_callback_data = list(map(int, btn_list[0].callback_data.split(':')[1:]))

    site_index = first_btn_callback_data[0]
    site = sites_index_module[site_index]
    theme_index = int(first_btn_callback_data[1])
    theme = list(site.phrases.keys())[theme_index]
    page = int(first_btn_callback_data[4])


    backward_btn = InlineKeyboardButton(text=LEXICON_RU['backward'],
                                        callback_data=PaginationCallbackFactory(
                                        stream='b', site_id=site_index, theme_id=theme_index, page_id=page).pack())
    pagination_btn = InlineKeyboardButton(text=f'{page} / {(len(site.phrases[theme]) + 5) // 6}',
                                          callback_data=PaginationCallbackFactory(
                                          stream='n', site_id=site_index, theme_id=theme_index, page_id=page).pack())
    forward_btn = InlineKeyboardButton(text=LEXICON_RU['forward'],
                                       callback_data=PaginationCallbackFactory(
                                       stream='f', site_id=site_index, theme_id=theme_index, page_id=page).pack())

    btn_list.append(backward_btn)
    result_builder = InlineKeyboardBuilder().row(*btn_list, width=1).add(pagination_btn, forward_btn)

    return result_builder.as_markup()



class PhrasesCallbackFactory(CallbackData, prefix='phrase'):
    site_id: int
    theme_id: int
    phrase_id: int
    lang_id: int
    page_id: int


# sites +
def phrase_keyboard_1(theme_callback_data: str) -> InlineKeyboardMarkup:
    """ПОЛЬЗОВАТЕЛЬ НАЖАЛ НА ТЕМУ"""
    # "theme site" <- callback
    callback_data = theme_callback_data.split()

    site_index = int(callback_data[1])
    site = sites_index_module[site_index]
    theme_index = int(callback_data[0])
    theme = list(site.phrases.keys())[theme_index]

    # вынеси page_size в глобал перем
    phr = []
    page_size = 6
    page_var = 0
    for i, eng in enumerate(site.phrases[theme]):
        if i % page_size == 0:
            page_var += 1
        phr.append(InlineKeyboardButton(text=eng,
                                        callback_data=PhrasesCallbackFactory(site_id=site_index,
                                                                             theme_id=theme_index,
                                                                             phrase_id=i,
                                                                             lang_id=0,
                                                                             page_id=page_var).pack()))

    return pagination_add_func(phr[:6])


#sites +
def phrase_keyboard_2(phrase_callback_data: str):
    """"ПОЛЬЗОВАТЕЛЬ НАЖАЛ НА ФРАЗУ"""
    # site:theme:phrase:lang:page
    callback_data = list(map(int, phrase_callback_data.split(':')[1:]))

    site_index = callback_data[0]
    site = sites_index_module[site_index]
    theme_index = callback_data[1]
    theme = list(site.phrases.keys())[theme_index]
    phrase_index = callback_data[2]
    lang_index = callback_data[3]
    page = callback_data[4]

    phr = []
    page_size = 6
    page_var = 0
    for i, eng in enumerate(site.phrases[theme]):
        if i % page_size == 0:
            page_var += 1
        phr.append(InlineKeyboardButton(text=eng,
                                        callback_data=PhrasesCallbackFactory(site_id=site_index,
                                                                             theme_id=theme_index,
                                                                             phrase_id=i,
                                                                             lang_id=0,
                                                                             page_id=page_var).pack()))

    # нажав "переворачиваю" карточку, на которую пришел апдейт с этим callback_data
    eng = phr[phrase_index]
    my_text = site.phrases[theme][eng.text] if lang_index == 0 else eng.text

    phr[phrase_index] = InlineKeyboardButton(text=my_text,
                                            callback_data=PhrasesCallbackFactory(site_id=site_index,
                                                                                 theme_id=theme_index,
                                                                                 phrase_id=phrase_index,
                                                                                 lang_id=(lang_index+1)%2,
                                                                                 page_id=page).pack())

    return pagination_add_func(phr[(page-1)*6:page*6])


# -------------------------pagination_theme_keyboard-(interaction started)-------------------------

class PaginationCallbackFactory(CallbackData, prefix='pagination'):
    stream: str     # b / n / f
    site_id: int
    theme_id: int
    page_id: int


# site +
def pagination_keyboard(callback: str) -> InlineKeyboardMarkup:
    """"ПОЛЬЗОВАТЕЛЬ НАЖАЛ НА КНОПКУ ПАГИНАЦИИ"""
    # прилетает pagination:f:0:2:1, а не phrase:0:2:0:0:1
    # stream:site:theme:page
    callback_data = callback.split(':')[1:]

    stream: str = callback_data[0]
    site_index = int(callback_data[1])
    site = sites_index_module[site_index]
    theme_index: int = int(callback_data[2])
    theme = list(site.phrases.keys())[theme_index]
    page = int(callback_data[3])

    if page > len(site.phrases[theme])+5//6:
        raise IndexError

    phr = []
    page_size = 6
    page_var = 0
    for i, eng in enumerate(site.phrases[theme]):
        if i % page_size == 0:
            page_var += 1
        phr.append(InlineKeyboardButton(text=eng,
                                        callback_data=PhrasesCallbackFactory(site_id=site_index,
                                                                             theme_id=theme_index,
                                                                             phrase_id=i,
                                                                             lang_id=0,
                                                                             page_id=page_var).pack()))

    if stream == 'f':
        return pagination_add_func(phr[page*6:(page+1)*6])
    elif stream == 'b':
        return pagination_add_func(phr[(page-2)*6:(page-1)*6])
