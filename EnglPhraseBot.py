from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = '7457980077:AAEM1VMCaTp-RtZ3HIS-E6t8ZzQTHOxS_r8'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    """ХЭНДЛЕР ДЛЯ ОБРАБОТКИ КОМАНДЫ '\\start'"""
    await message.answer('Привет!\nДавай учить популярные фразы в английском со мной!')

@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    """ХЭНДЛЕР ДЛЯ ОБРАБОТКИ КОМАНДЫ '\\help'"""
    await message.answer(
        'В боте есть следующий функционал:\n'
        'Х - периодичность появления фразы\n'
        'У - тема фраз\n'
        'Z - отключить отправку фраз\n'
    )

@dp.message(F.photo)
async def process_photo_command(message: Message):
    await message.answer_photo(message.photo[0].file_id)

@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Метод send_copy не поддерживает такой тип апдейтов')


dp.run_polling(bot)