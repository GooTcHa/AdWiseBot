from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


class QueryDataFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, query: CallbackQuery) -> bool:
        return query.data == self.my_text
