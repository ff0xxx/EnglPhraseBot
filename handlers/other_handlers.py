from aiogram import Router, F
from lexicon import LEXICON_RU
from aiogram.types import Message

router: Router = Router()

@router.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])

@router.message(F.photo)
async def process_photo_command(message: Message):
    await message.answer_photo(message.photo[0].file_id)
