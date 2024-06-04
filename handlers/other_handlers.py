import aiogram.exceptions
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import skyeng_inline_keyboard
from lexicon.lexicon_ru import LEXICON_RU


router: Router = Router()


@router.message(F.text == 'skyeng (100)')
async def process_skyeng_answer(message: Message):
    """хендлер кнопки (выбора сайта): skyeng"""
    await message.answer(text=f'{message.chat.first_name}, выбери тему:\n',
                         reply_markup=skyeng_inline_keyboard)


@router.callback_query()
async def skyeng_btn_answer(callback: CallbackQuery):
    """хендлер кнопки btn (skyeng)"""
    try:
        await callback.message.edit_text(
            text=callback.data + '\n\nЧто-то будет происходить после нажатия этой кнопки\n'
                               'Можно новую Inline клавиатуру прикрепить, но я оставлю старую',
            reply_markup=callback.message.reply_markup
        )
    except aiogram.exceptions.TelegramBadRequest:
        if callback.from_user.id == 5844230371:
            await callback.answer(text="I'm watching you=)", show_alert=True)
        await callback.answer(text='Один гордится тобой!')


@router.message()
async def send_echo(message: Message):
    """ХЭНДЛЕР ДЛЯ ОБРАБОТКИ НЕОЖИДАННЫХ СООБЩЕНИЙ"""
    try:
        await message.reply(text=LEXICON_RU['echo'])
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])