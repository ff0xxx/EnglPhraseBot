from aiogram.types                  import (KeyboardButton, ReplyKeyboardMarkup,
                                            InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
from aiogram.filters.callback_data  import CallbackData
from aiogram.utils.keyboard         import InlineKeyboardBuilder
from parsers                        import skyeng
from lexicon.lexicon_ru             import LEXICON_RU

# -------------------------| select_site_keyboard |----------------------------


def select_site_keyboard() -> ReplyKeyboardMarkup:
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
        input_field_placeholder='Кнопки нажимай, дубина')

    return keyboard


# -------------------------| skyeng_inline_keyboard |---------------------------

def skyeng_inline_keyboard() -> InlineKeyboardMarkup:
    """ДЕЛАЮ INLINE-КЛАВИАТУРУ ДЛЯ ТЕМ ИЗ skyeng"""
    btns = [InlineKeyboardButton(text=theme, callback_data=str(i)) for i, theme in enumerate(skyeng.themes_list)]
    btn0 = InlineKeyboardButton(text='link',
                                url=skyeng.URL)

    builder = InlineKeyboardBuilder().row(*btns, width=1).add(btn0)
    return builder.as_markup()


# -------------------------| pagination_add_func |---------------------------

def pagination_add_func(btn_list: list[InlineKeyboardButton]) -> InlineKeyboardMarkup:
    """ИЗ СПИСКА INLINE-КНОПОК ДЕЛАЮ PAGINATION-КЛАВИАТУРУ"""
    print('BTN_LIST: ', btn_list)

    # site:theme:phrase:lang:page
    first_btn_callback = btn_list[0].callback_data.split(':')[1:]

    page = int(first_btn_callback[4])

    theme_index = int(first_btn_callback[1])
    theme = list(skyeng.phrases.keys())[theme_index]

    backward_btn = InlineKeyboardButton(text=LEXICON_RU['backward'],
                                        callback_data=PaginationCallbackFactory(
                                        stream='b', site_id=0, theme_id=theme_index, page_id=page).pack())
    pagination_btn = InlineKeyboardButton(text=f'{page} / {(len(skyeng.phrases[theme]) + 5) // 6}',
                                          callback_data=PaginationCallbackFactory(
                                          stream='n', site_id=0, theme_id=theme_index, page_id=page).pack())
    forward_btn = InlineKeyboardButton(text=LEXICON_RU['forward'],
                                       callback_data=PaginationCallbackFactory(
                                       stream='f', site_id=0, theme_id=theme_index, page_id=page).pack())

    btn_list.append(backward_btn)
    result_builder = InlineKeyboardBuilder().row(*btn_list, width=1).add(pagination_btn, forward_btn)

    return result_builder.as_markup()


# -------------------------| skyeng_callback_keyboard |-------------------------


class PhrasesCallbackFactory(CallbackData, prefix='phrase'):
    site_id: int
    theme_id: int
    phrase_id: int
    lang_id: int
    page_id: int


# need to sent only 6 first btns
def theme_keyboard(theme_index: str) -> InlineKeyboardMarkup:
    """КОГДА ПОЛЬЗОВАТЕЛЬ НАЖАЛ ТЕМУ"""
    theme = list(skyeng.phrases.keys())[int(theme_index)]

    phr = []
    page_size = 6
    page_var = 0
    for i, eng in enumerate(skyeng.phrases[theme]):
        if i % page_size == 0:
            page_var += 1
        phr.append(InlineKeyboardButton(text=eng,
                                        callback_data=PhrasesCallbackFactory(site_id=0,
                                                                             theme_id=theme_index,
                                                                             phrase_id=i,
                                                                             lang_id=0,
                                                                             page_id=page_var).pack()))

    return pagination_add_func(phr[:6])


# -------------------| skyeng_callback_keyboard-(interaction started) |-----------------


def phrase_keyboard(callback_data: str, page=0):
    """"КОГДА ПОЛЬЗОВАТЕЛЬ ПОСЛЕ ТЕМЫ НАЖАЛ НА ФРАЗУ (А НЕ КНОПКУ ПАГИНАЦИИ)"""

    # site:theme:phrase:lang:page <-- получаю параметры определенной КНОПКИ
    callback = list(map(int, callback_data.split(':')[1:]))

    theme = list(skyeng.phrases.keys())[int(callback[1])]
    page = int(callback[4])

    phr = []
    page_size = 6
    page_var = 0
    for i, eng in enumerate(skyeng.phrases[theme]):
        if i % page_size == 0:
            page_var += 1
        phr.append(InlineKeyboardButton(text=eng,
                                        callback_data=PhrasesCallbackFactory(site_id=0,
                                                                             theme_id=callback[1],
                                                                             phrase_id=i,
                                                                             lang_id=0,
                                                                             page_id=page_var).pack()))

    # нажав "переворачиваю" карточку, на которую пришел апдейт с этим callback_data
    eng = phr[callback[2]]
    my_text = skyeng.phrases[theme][eng.text] if callback[3] == 0 else eng.text

    phr[callback[2]] = InlineKeyboardButton(text=my_text,
                                            callback_data=PhrasesCallbackFactory(site_id=0,
                                                                                 theme_id=callback[1],
                                                                                 phrase_id=callback[2],
                                                                                 lang_id=(callback[3]+1)%2,
                                                                                 page_id=page).pack())

    return pagination_add_func(phr[(page-1)*6:page*6])


# -------------------------pagination_theme_keyboard-(interaction started)-------------------------

class PaginationCallbackFactory(CallbackData, prefix='pagination'):
    stream: str     # b / n / f
    site_id: int
    theme_id: int
    page_id: int


def pagination_theme_keyboard(callback: str) -> InlineKeyboardMarkup:
    """"КОГДА ПОЛЬЗОВАТЕЛЬ ПОСЛЕ ТЕМЫ НАЖАЛ НА КНОПКУ ПАГИНАЦИИ (А НЕ ФРАЗУ)"""

    # stream:site:theme:page
    callback_data = callback.split(':')[1:]

    stream = callback_data[0]
    page = int(callback_data[3])
    theme_index: int = int(callback_data[2])
    theme = list(skyeng.phrases.keys())[theme_index]

    if page > len(skyeng.phrases[theme])+5//6:
        raise IndexError

    phr = []
    page_size = 6
    page_var = 0
    for i, eng in enumerate(skyeng.phrases[theme]):
        if i % page_size == 0:
            page_var += 1
        phr.append(InlineKeyboardButton(text=eng,
                                        callback_data=PhrasesCallbackFactory(site_id=0,
                                                                             theme_id=theme_index,
                                                                             phrase_id=i,
                                                                             lang_id=0,
                                                                             page_id=page_var).pack()))

    if stream == 'f':
        return pagination_add_func(phr[page*6:(page+1)*6])
    elif stream == 'b':
        return pagination_add_func(phr[(page-2)*6:(page-1)*6])
