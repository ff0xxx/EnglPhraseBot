import logging
from aiogram            import Bot, Dispatcher
from asyncio            import run
from config_data.config import Config, load_config
from handlers           import user_handlers, other_handlers, trol
from keyboards.set_menu import set_main_menu


logger = logging.getLogger(__name__)

async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s ->[%(actime)s]<- %(name)s %(message)s'
    )

    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(trol.router)
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    dp.startup.register(set_main_menu)

    logger.info('Starting bot')

    await bot.delete_webhook(drop_pending_updates=True)  # LoL
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())