import aiogram.exceptions
from aiogram                import Router, F
from aiogram.types          import Message, CallbackQuery
from keyboards.keyboards    import (PhrasesCallbackFactory, skyeng_inline_keyboard,
                                    theme_keyboard, pagination_theme_keyboard, phrase_keyboard)
from filters.filters        import IsForwardCallbackData, IsBackwardCallbackData, IsStayCallbackData
from lexicon.lexicon_ru     import LEXICON_RU


router: Router = Router()


@router.callback_query(IsForwardCallbackData())
async def process_forward_press(callback: CallbackQuery):
    """хендлер кнопки (ВПЕРЕД): пагинация"""

    try:
        await callback.message.edit_text(
            text=callback.data + LEXICON_RU['forth'],
            reply_markup=pagination_theme_keyboard(callback.data)
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
            reply_markup=pagination_theme_keyboard(callback.data)
        )
    except aiogram.exceptions.TelegramBadRequest:
        await callback.answer(text=LEXICON_RU['back process'])
    except IndexError:
        await callback.answer(text=LEXICON_RU['pages end'])


@router.callback_query(IsStayCallbackData())
async def process_backward_press(callback: CallbackQuery):
    """хендлер кнопки (СТОЙ): пагинация"""

    await callback.answer(text=LEXICON_RU['stay'], show_alert=True)


@router.callback_query(PhrasesCallbackFactory.filter())
async def phrase_keyboard_answer(callback: CallbackQuery):
    """хендлер кнопки (ФРАЗЫ): skyeng"""
    # сюда летит с колбеком -> phrase:0:2:1
    try:
        await callback.message.edit_text(
            text=callback.data + LEXICON_RU['phrase'],
            reply_markup=phrase_keyboard(callback.data),
        )
    except aiogram.exceptions.TelegramBadRequest:
        await callback.answer(text=LEXICON_RU['phrase process'])


@router.message(F.text == 'skyeng (100)')
async def process_skyeng_answer(message: Message):
    """хендлер кнопки (выбора ТЕМЫ): skyeng"""
    try:
        await message.answer(text=LEXICON_RU['theme'],
                             reply_markup=skyeng_inline_keyboard())
    except aiogram.exceptions.TelegramBadRequest:
        await message.answer(text=LEXICON_RU['theme process'])

@router.callback_query()
async def skyeng_btn_answer(callback: CallbackQuery):
    """хендлер кнопки (САЙТА): skyeng"""
    try:
        await callback.message.edit_text(
            text=callback.data + LEXICON_RU['site'],
            reply_markup=theme_keyboard(callback.data)
        )
    except aiogram.exceptions.TelegramBadRequest:
        await callback.answer(text=LEXICON_RU['site process'])


@router.message()
async def send_echo(message: Message):
    """ХЭНДЛЕР ДЛЯ ОБРАБОТКИ НЕОЖИДАННЫХ СООБЩЕНИЙ"""
    try:
        await message.reply(text=LEXICON_RU['echo'])
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])