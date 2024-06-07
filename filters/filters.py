from aiogram.filters    import BaseFilter
from aiogram.types      import CallbackQuery


class IsForwardCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        try:
            return callback.data.split(':')[1] == 'f'
        except Exception:
            return False


class IsBackwardCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        try:
            return callback.data.split(':')[1] == 'b'
        except Exception:
            return False


class IsStayCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        try:
            return callback.data.split(':')[1] == 'n'
        except Exception:
            return False
