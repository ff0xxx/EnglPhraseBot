from aiogram import Router, F
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.keyboards import skyeng_keyboard


router: Router = Router()


@router.message(F.text == 'иди нахуй')
async def process_mat_answer(message: Message):
    await message.reply(text='Сам иди нахуй=)',
                        reply_markup=ReplyKeyboardRemove())


@router.message(F.text == 'skyeng (100)')
async def process_btn1_answer(message: Message):
    await message.answer(text=f'{message.chat.first_name} {message.chat.last_name}, выбери тему:\n',
                         reply_markup=skyeng_keyboard)


@router.message()
async def send_echo(message: Message):
    try:
        await message.reply(text=LEXICON_RU['echo'])
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])
