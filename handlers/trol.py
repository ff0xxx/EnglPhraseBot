from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router: Router = Router()

router.message.filter(lambda msg: str(msg.chat.id) == '00000000')


@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    """ХЭНДЛЕР ДЛЯ ОБРАБОТКИ КОМАНДЫ '\\start'"""
    await message.answer('сука,\n баля,\n Greg))')
