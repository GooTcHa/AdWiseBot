import asyncio
import logging
import sys

import aiomysql
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, and_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiohttp import web

import client
import speс
import admin

import config
import db

import keyboards
import msg
from filters import QueryDataFilter
from states import User, Worker, Client

TOKEN = config.token

dp = Dispatcher()

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

# app = web.Application()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    # TODO проверка пользователя на бан
    try:
        if not await db.if_user_exists(message.from_user.id):
            await db.update_user_data(message.from_user.id, f'@{message.from_user.username}', False)
        else:
            await db.update_user_data(message.from_user.id, f'@{message.from_user.username}', True)
        await state.clear()
        # await state.set_state(User.choose_start_action)
        await message.answer(f"{await msg.start_message(message.from_user.username)}",
                             reply_markup=await keyboards.get_start_ikb())
    except Exception as ex:
        print(f'Exception in \\start:\n\t{ex}')
        await message.answer(text=msg.errorMessage, reply_markup=await keyboards.delete_kbd())


@dp.message(Command("menu"))
async def command_menu_handler(message: Message, state: FSMContext) -> None:
    try:
        await state.clear()
        # await state.set_state(User.choose_start_action)
        await message.answer(f"Что вы ищите?",
                             reply_markup=await keyboards.get_start_ikb())
    except Exception as ex:
        print(f'Exception in \\start:\n\t{ex}')
        await message.answer(text=msg.errorMessage, reply_markup=await keyboards.delete_kbd())


@dp.message(Command("specmenu"))
async def command_specmenu_handler(message: Message, state: FSMContext) -> None:
    try:
        await state.clear()
        await state.set_state(Worker.menu)
        await message.answer(text='Меню специалиста🏢', reply_markup=await keyboards.worker_menu())
    except Exception as ex:
        print(f'Exception in \\start:\n\t{ex}')
        await message.answer(text=msg.errorMessage, reply_markup=await keyboards.delete_kbd())


@dp.message(Command("customermenu"))
async def command_customermenu_handler(message: Message, state: FSMContext) -> None:
    try:
        await state.clear()
        await state.set_state(Client.menu)
        await message.answer(text='Добро пожаловать в меню заказчика🧑‍💻',
                             reply_markup=await keyboards.client_menu())
    except Exception as ex:
        print(f'Exception in \\start:\n\t{ex}')
        await message.answer(text=msg.errorMessage, reply_markup=await keyboards.delete_kbd())


# async def set_webhook():
#     webhook_uri = f'{config.webhook_url}{config.webhook_path}'
#     await bot.set_webhook(
#         webhook_uri
#     )


# async def on_startup(_):
#     print('f\nf\n')
#     db.conn = await aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
#                                      password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop())
#     dp.include_routers(
#         speс.router,
#         client.router,
#         admin.router
#     )
#
#     await bot.delete_webhook(drop_pending_updates=True)
#
#     await set_webhook()
#
#
# async def on_shutdown(_):
#     db.conn.close()
#
#
# async def handle_webhook(request):
#     print(request)
#     url = str(request.url)
#     index = url.rfind('/')
#     token = url[index + 1:]
#     print(f'#\n#\n#\n#\n{token}')
#     if token == config.token:
#         update = types.Update.model_validate(await request.json(), context={"bot": bot})
#         await dp.feed_update(bot=bot, update=update)
#         return web.Response()
#     else:
#         return web.Response(status=403)


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_routers(
        speс.router,
        client.router,
        admin.router
    )
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    # app.router.add_post(f'/{config.token}', handle_webhook)
    # app.on_startup.append(on_startup)
    # app.on_shutdown.append(on_shutdown)
    #
    # web.run_app(
    #     app,
    #     host='0.0.0.0',
    #     port=config.webhook_port
    # )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     main()
