import aiogram.exceptions
from aiogram                import Router, F
from aiogram.types          import Message, CallbackQuery
from keyboards.keyboards    import (PhrasesCallbackFactory, skyeng_inline_keyboard,
                                    theme_keyboard, pagination_theme_keyboard, phrase_keyboard)
from filters.filters        import IsForwardCallbackData, IsBackwardCallbackData, IsNCallbackData
from lexicon.lexicon_ru     import LEXICON_RU


router: Router = Router()


@router.message(F.text == 'skyeng (100)')
async def process_skyeng_answer(message: Message):
    """хендлер кнопки (выбора САЙТА): skyeng"""
    try:
        await message.answer(text='Выберите тему фраз:\n',
                             reply_markup=skyeng_inline_keyboard())
    except aiogram.exceptions.TelegramBadRequest:
        await message.answer(text='Ты уже нажал на тему!')


@router.callback_query(IsForwardCallbackData())
async def process_forward_press(callback: CallbackQuery):
    """хендлер кнопки (ВПЕРЕД): пагинация"""

    try:
        await callback.message.edit_text(
            text=callback.data + '\n\nВы пролистнули вперед',
            reply_markup=pagination_theme_keyboard(callback.data)
            #reply_markup=callback.message.reply_markup
        )
    except aiogram.exceptions.TelegramBadRequest:
        await callback.answer(text='Вы переходите на следующую страницу')
    except IndexError:
        await callback.answer(text='Шалунишка)\nВидишь же, что страницы кончились')


@router.callback_query(IsBackwardCallbackData())
async def process_backward_press(callback: CallbackQuery):
    """хендлер кнопки (НАЗАД): пагинация"""

    try:
        await callback.message.edit_text(
            text=callback.data + '\n\nВы пролистнули назад',
            reply_markup=pagination_theme_keyboard(callback.data)
        )
    except aiogram.exceptions.TelegramBadRequest:
        await callback.answer(text='Вы переходите на предыдущую страницу')
    except IndexError:
        await callback.answer(text='Шалунишка)\nВидишь же, что страницы кончились')


@router.callback_query(IsNCallbackData())
async def process_backward_press(callback: CallbackQuery):
    """хендлер кнопки (СТОЙ): пагинация"""

    await callback.answer(text='Этот функционал еще не проработан', show_alert=True)


@router.callback_query(PhrasesCallbackFactory.filter())
async def phrase_keyboard_answer(callback: CallbackQuery):
    """хендлер кнопки (ФРАЗЫ): skyeng"""
    # сюда летит с колбеком -> phrase:0:2:1
    print('CALLBACK.DATA 2 (передаю): ------------>', callback.data)
    try:
        await callback.message.edit_text(
            text=callback.data + '\n\nИдет работа с карточками',
            reply_markup=phrase_keyboard(callback.data),
        )
    except aiogram.exceptions.TelegramBadRequest:
        await callback.answer(text='Ты уже нажал на фразу')


@router.callback_query()
async def skyeng_btn_answer(callback: CallbackQuery):
    """хендлер кнопки (ТЕМЫ): skyeng"""
    try:
        print('CALLBACK.DATA (передаю): ------------>', callback.data)
        await callback.message.edit_text(
            text=callback.data + '\n\nИдет работа с карточками',
            # ?????
            reply_markup=theme_keyboard(callback.data)
        )
    except aiogram.exceptions.TelegramBadRequest:
        await callback.answer(text='Ты переходишь в режим работы с карточками!')


@router.message()
async def send_echo(message: Message):
    """ХЭНДЛЕР ДЛЯ ОБРАБОТКИ НЕОЖИДАННЫХ СООБЩЕНИЙ"""
    try:
        await message.reply(text=LEXICON_RU['echo'])
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])