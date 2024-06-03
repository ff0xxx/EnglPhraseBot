from aiogram            import Bot
from aiogram.types      import BotCommand


async def set_main_menu(bot: Bot):

    main_menu_commands = [
        BotCommand(command='/start', description='Не твоего ума дело'),
        BotCommand(command='/help', description='Тебя ебать не должно')
    ]

    await bot.set_my_commands(main_menu_commands)