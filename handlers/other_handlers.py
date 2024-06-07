import aiogram.exceptions
from aiogram                import Router, F
from aiogram.types          import Message, CallbackQuery
from keyboards.keyboards    import (PhrasesCallbackFactory, theme_keyboard,
                                    phrase_keyboard_1, pagination_keyboard, phrase_keyboard_2)
from filters.filters        import IsForwardCallbackData, IsBackwardCallbackData, IsStayCallbackData
from lexicon.lexicon_ru     import LEXICON_RU


router: Router = Router()


@router.callback_query(IsForwardCallbackData())
async def process_forward_press(callback: CallbackQuery):
    """хендлер кнопки (ВПЕРЕД): пагинация"""

    try:
        await callback.message.edit_text(
            text=callback.data + LEXICON_RU['forth'],
            reply_markup=pagination_keyboard(callback.data)
            #reply_markup=callback.message.reply_markup
        )
    except aiogram.exceptions.TelegramBadRequest:
        await callback.answer(text=LEXICON_RU['forth process'])
    except IndexError:
        await callback.answer(text=LEXICON_RU['pages end'])


@router.callback_query(IsBackwardCallbackData())
async def process_backward_press(callback: CallbackQuery):
    """хендлер кнопки (НАЗАД): пагинация"""
    try:
        await callback.message.edit_text(
            text=callback.data + LEXICON_RU['back'],
            reply_markup=pagination_keyboard(callback.data)
        )
    except aiogram.exceptions.TelegramBadRequest:
        await callback.answer(text=LEXICON_RU['back process'])
    except IndexError:
        await callback.answer(text=LEXICON_RU['pages end'])


@router.callback_query(IsStayCallbackData())
async def process_stay_press(callback: CallbackQuery):
    """хендлер кнопки (СТОЙ): пагинация"""
    await callback.answer(text=LEXICON_RU['stay'], show_alert=True)


#sites +
@router.callback_query(PhrasesCallbackFactory.filter())
async def process_phrases_press_2(callback: CallbackQuery):
    """хендлер кнопки (ФРАЗЫ 2) -- модифицируются кнопки process_phrases_press_1"""
    try:
        await callback.message.edit_text(
            text=callback.data + LEXICON_RU['phrase'],
            reply_markup=phrase_keyboard_2(callback.data),
        )
    except aiogram.exceptions.TelegramBadRequest:
        await callback.answer(text=LEXICON_RU['phrase process'])


#sites +
@router.callback_query()
async def process_phrases_press_1(callback: CallbackQuery):
    """хендлер кнопки (ФРАЗЫ 1)"""
    try:
        await callback.message.edit_text(
            text=callback.data + LEXICON_RU['phrase'],
            reply_markup=phrase_keyboard_1(callback.data)
        )
    except aiogram.exceptions.TelegramBadRequest:
        await callback.answer(text=LEXICON_RU['phrase process'])


# sites +
@router.message((F.text == 'skyeng (100)') | (F.text == 'smileenglish (200)') | (F.text == 'lingua-academ (380)'))
async def process_theme_press(message: Message):
    """хендлер кнопки (выбора ТЕМЫ)"""
    try:
        site = message.text.split()[0]
        await message.answer(text=LEXICON_RU['theme'],
                             reply_markup=theme_keyboard(site))
    except aiogram.exceptions.TelegramBadRequest:
        await message.answer(text=LEXICON_RU['theme process'])


@router.message()
async def send_echo(message: Message):
    """ХЭНДЛЕР ДЛЯ ОБРАБОТКИ НЕОЖИДАННЫХ СООБЩЕНИЙ"""
    try:
        await message.reply(text=LEXICON_RU['echo'])
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])