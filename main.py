from aiogram            import Bot, Dispatcher
from config_data.config import Config, load_config
from asyncio            import run
from handlers           import user_handlers, other_handlers, trol


async def main() -> None:
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    dp.include_router(trol.router)
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)  # LoL
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())