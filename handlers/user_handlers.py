from aiogram                import Router, F
from aiogram.filters        import Command, ChatMemberUpdatedFilter, KICKED
from aiogram.types          import Message, ReplyKeyboardRemove, ChatMemberUpdated
from lexicon.lexicon_ru     import LEXICON_RU
from keyboards.keyboards    import site_keyboard


router: Router = Router()


@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    """ХЭНДЛЕР ДЛЯ ОБРАБОТКИ КОМАНДЫ '\\start'"""
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=site_keyboard())


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    """ХЭНДЛЕР ДЛЯ ОБРАБОТКИ КОМАНДЫ '\\help'"""
    await message.answer(LEXICON_RU['/help'])


# Этот хэндлер будет срабатывать на блокировку бота пользователем
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    print(f'Пользователь {event.from_user.id} заблокировал бота')


@router.message(F.text == 'иди нахуй')
async def process_mat_answer(message: Message):
    """ХЭНДЛЕР ДЛЯ ОБРАБОТКИ КОМАНДЫ МАТА"""
    await message.reply(text='Сам иди нахуй=)',
                        reply_markup=ReplyKeyboardRemove())
