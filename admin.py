import asyncio

from aiogram import Router, F
from aiogram.filters import and_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import config
import db
import keyboards
import main
import msg
from filters import QueryDataFilter
from states import Admin

router = Router(name=__name__)


@router.message(Admin.decline_cv_reason)
async def decline_cv_reason(message: Message, state:FSMContext):
    try:
        if message.chat.id == config.cv_id or config.projects_id or config.check_project_id:
            user_id = int(await db.delete_cv(message.text.split('\n')[0]))
            await state.clear()
            await main.bot.send_message(chat_id=user_id, text=f'Ваше резюме отклонено по причине: {message.text}',
                                        reply_markup=await keyboards.worker_menu_button())
            await message.answer(text='Сообщение отправлено')
    except Exception as ex:
        print(ex)


@router.message(Admin.decline_project_reason)
async def decline_project_reason(message: Message, state: FSMContext):
    try:
        if message.chat.id == config.cv_id or config.projects_id or config.check_project_id:
            info = (await state.get_data()).get('decline_project')
            await db.delete_projects(info[0])
            await state.clear()
            await main.bot.send_message(chat_id=info[1], text=f'Ваш заказ #{info[0]} удалён по причине: {message.text}',
                                        reply_markup=await keyboards.worker_menu_button())
            await message.answer(text='Сообщение отправлено')
    except Exception as ex:
        print(ex)


@router.callback_query(QueryDataFilter('accept_cv'))
async def accept_cv(query: CallbackQuery, state: FSMContext):
    try:
        if query.message.chat.id == config.cv_id or config.projects_id or config.check_project_id:
            user_id = int(query.message.text.split('\n')[0])
            if await db.accept_cv(user_id):
                await query.message.edit_text(text='Резюме одобрено!', reply_markup=await keyboards.delete_kbd())
                await main.bot.send_message(chat_id=user_id, text='Ваше резюме одобрено!',
                                            reply_markup=await keyboards.worker_menu_button())
            else:
                await query.message.answer(text='Что-то пошло не так')
    except Exception as ex:
        print(ex)


@router.callback_query(QueryDataFilter('decline_cv'))
async def accept_cv(query: CallbackQuery, state: FSMContext):
    try:
        if query.message.chat.id == config.cv_id or config.projects_id or config.check_project_id:
            await state.set_state(Admin.decline_cv_reason)
            await query.message.edit_text(text='Укажите причину отказа:', reply_markup=await keyboards.delete_kbd())
    except Exception as ex:
        print(ex)


@router.callback_query(QueryDataFilter('accept_project'))
async def accept_project(query: CallbackQuery, state: FSMContext):
    try:
        if query.message.chat.id == config.cv_id or config.projects_id or config.check_project_id:
            order_id = int(query.message.text.split('\n')[0])
            user_id = int(query.message.text.split('\n')[1])
            if await db.accept_project(order_id, user_id):
                await query.message.edit_text(text=f'Заказ #{order_id} одобрен!',
                                              reply_markup=await keyboards.delete_kbd())
                # await asyncio.sleep(60)
                await main.bot.send_message(chat_id=user_id, text=f'Ваш заказ #{order_id} одобрен!',
                                            reply_markup=await keyboards.client_menu_button())
            else:
                await query.message.answer(text='Что-то пошло не так')
    except Exception as ex:
        print(f'Exception: {ex}')


@router.callback_query(QueryDataFilter('decline_project'))
async def decline_project(query: CallbackQuery, state: FSMContext):
    try:
        if query.message.chat.id == config.cv_id or config.projects_id or config.check_project_id:
            await state.update_data(decline_project=[int(query.message.text.split('\n')[0]),
                                                     int(query.message.text.split('\n')[1])])
            await state.set_state(Admin.decline_project_reason)
            await query.message.edit_text(text='Укажите причину отказа:', reply_markup=await keyboards.delete_kbd())
    except Exception as ex:
        print(ex)
