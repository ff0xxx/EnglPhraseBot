from aiogram.filters    import BaseFilter
from aiogram.types      import CallbackQuery


class IsForwardCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        try:
            return callback.data.split(':')[1] == 'f'
        except Exception as e:
            print(e)
            return False


class IsBackwardCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        try:
            return callback.data.split(':')[1] == 'b'
        except Exception as e:
            print(e)
            return False


class IsStayCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        try:
            return callback.data.split(':')[1] == 'n'
        except Exception as e:
            print(e)
            return False
