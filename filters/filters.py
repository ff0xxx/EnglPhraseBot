from aiogram.filters    import BaseFilter
from aiogram.types      import CallbackQuery


class IsForwardCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        try:
            return callback.data.split(':')[1] == 'f'
        except Exception as e:
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


class ShitFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        try:
            return callback.data == 'sad'
        except Exception:
            return False
