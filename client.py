import asyncio

from aiogram import Router, F
from aiogram.filters import and_f, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import config
import db
import msg
import keyboards
from filters import QueryDataFilter
from states import User, Worker, Client
from main import bot

router = Router(name=__name__)


@router.callback_query(QueryDataFilter('looking_for_specialists'))
async def client_menu(query: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await state.set_state(Client.menu)
        await query.message.edit_text(text='Добро пожаловать в меню заказчика🧑‍💻',
                                      reply_markup=await keyboards.client_menu())
    except Exception as ex:
        print(f'Error in client menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(QueryDataFilter('buy_subscription'))
async def buy_subscription(query: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        if await db.buy_basic_subscription(query.from_user.id):
            await query.answer(text='Подписка успешно оформлена!', cache_time=3)
            order = await db.get_unsubscribed_projects(query.from_user.id)
            await bot.send_message(chat_id=config.projects_id, text=f'{order[1]}\n{query.from_user.id}\n\n'
                                                                    f'Название проекта: {order[2]}\n'
                                                                    f'Необходимый специалист: {order[3]}\n'
                                                                    f'Описание задачи: {order[4]}\n'
                                                                    f'Бюджет: {order[5]}BYN\n',
                                   reply_markup=await keyboards.accept_project_ikb())
            await query.message.edit_text(text='Подписка успешно оформлена!\nТеперь вы можете искать специалистов!',
                                          reply_markup=await keyboards.client_menu())
        else:
            await query.answer(text='Упс...\nПопробуйте позже')
            await asyncio.sleep(3)

    except Exception as ex:
        print(f'Error in search_spec:\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(QueryDataFilter('client_projects'))
async def client_projects(query: CallbackQuery, state: FSMContext):
    await state.clear()
    if await db.check_user_projects_count(query.from_user.id) > 0:
        await state.set_state(Client.project_list)
        # await query.message.edit_text(text='Выберите проект на который вы хотите найти специалиста:',
        #                               reply_markup=await keyboards.delete_kbd())
        projects = await db.get_user_projects(query.from_user.id)
        if len(projects) != 0:
            await state.update_data(projects_info=[projects, 0, len(projects)])
            await query.message.edit_text(text=await msg.display_project(projects[0], f'1/{len(projects)}'),
                                          reply_markup=await keyboards.project_list())
        else:
            await state.clear()
            await query.message.edit_text(text='Все ваши проекты, пока ожидают подтверждения!')
    else:
        await state.set_state(Client.ask_create_project)
        await query.message.edit_text(text='У вас пока нет проектов😭\nХотите создать?',
                                      reply_markup=await keyboards.ask_create_project())
    # try:
    #     await state.clear()
    #     if await db.check_user_projects_count(query.from_user.id) > 0:
    #         await state.set_state(Client.project_list)
    #         projects = await db.get_user_projects(query.from_user.id)
    #         if projects != ():
    #             await state.update_data(projects_info=[projects, 0, len(projects)])
    #             # await query.message.edit_text(text='Ваши проекты:', reply_markup=await keyboards.delete_kbd())
    #             await query.message.edit_text(text=await msg.display_project(projects[0], f'1/{len(projects)}'),
    #                                           reply_markup=await keyboards.project_list())
    #         else:
    #             await state.clear()
    #             await query.message.edit_text(text='Все ваши проекты, пока ожидают подтверждения!')
    #     else:
    #         await state.set_state(Client.ask_create_project)
    #         await query.message.edit_text(text='У вас пока нет проектов😭\nХотите создать?',
    #                                       reply_markup=await keyboards.ask_create_project())
    # except Exception as ex:
    #     print(f'Error in client_projects menu\n{ex}')
    #     await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(or_f(QueryDataFilter('0'), QueryDataFilter('1')), Client.ask_create_project))
async def ask_create_project(query: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        if int(query.data):
            await state.set_state(Client.enter_title)
            await query.message.edit_text(text='Хорошо, приступим к созданию проекта\nВведите название вашего проекта:',
                                          reply_markup=await keyboards.delete_kbd())
        else:
            await state.set_state(Client.menu)
            await query.message.edit_text(text='Добро пожаловать в меню заказчика🧑‍💻',
                                          reply_markup=await keyboards.client_menu())
    except Exception as ex:
        print(f'Error in client_projects menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(QueryDataFilter('search_spec'))
async def search_spec(query: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        if await db.check_user_projects_count(query.from_user.id) > 0:
            await state.set_state(Client.choose_project)
            # await query.message.edit_text(text='Выберите проект на который вы хотите найти специалиста:',
            #                               reply_markup=await keyboards.delete_kbd())
            projects = await db.get_user_projects(query.from_user.id)
            if len(projects) != 0:
                await state.update_data(projects_info=[projects, 0, len(projects)])
                await query.message.edit_text(text=await msg.display_project(projects[0], f'1/{len(projects)}'),
                                              reply_markup=await keyboards.project_menu())
            else:
                await state.clear()
                await query.message.edit_text(text='Все ваши проекты, пока ожидают подтверждения!')
        else:
            await state.set_state(Client.ask_create_project)
            await query.message.edit_text(text='У вас пока нет проектов😭\nХотите создать?',
                                          reply_markup=await keyboards.ask_create_project())

    except Exception as ex:
        print(f'Error in search_spec:\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(QueryDataFilter('create_project'))
async def create_project(query: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        sub_status = await db.if_user_can_create_project(query.from_user.id)
        if sub_status == 2 or -1:
            await state.set_state(Client.enter_title)
            await query.message.edit_text(text='Хорошо, приступим к созданию проекта\nВведите название вашего проекта:',
                                          reply_markup=await keyboards.delete_kbd())

        elif sub_status == 1:
            await query.message.edit_text(text='У вас уже создано максимально возможное количество проектов\n'
                                               'Для снятия ограничения оформите подписку MAX',
                                          reply_markup=await keyboards.ask_buy_max())
        elif sub_status == 0:
            # TODO buy subscription
            await query.message.edit_text(text='Для того, чтобы создать новый заказ необходимо оформить подписку!',
                                          reply_markup=await keyboards.buy_subscription())

    except Exception as ex:
        print(f'Error in create_project menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.message(Client.enter_title)
async def enter_title(message: Message, state: FSMContext):
    try:
        await state.update_data(enter_title=message.text)
        await state.set_state(Client.choose_spec)
        await message.answer(text='Отличное название! Выберите необходимого специалиста:',
                             reply_markup=await keyboards.get_specialists_ikb())
    except Exception as ex:
        print(f'Error in create_project menu\n{ex}')
        await message.answer(text=msg.errorMessage)


@router.callback_query(Client.choose_spec)
async def choose_spec(query: CallbackQuery, state: FSMContext):
    try:
        if query.data in config.specialties:
            if query.data == config.specialties[-1]:
                await state.set_state(Client.add_new_specialty)
                # TODO new specialties
                await query.message.edit_text('Введите название нужной специализации и мы добавим её в ближайшем '
                                              'времени:',
                                              reply_markup=await keyboards.delete_kbd())
            else:
                await state.update_data(choose_speс=query.data)
                await state.set_state(Client.enter_descr)
                await query.message.edit_text(text='Класс!\nОпишите суть задачи:',
                                              reply_markup=await keyboards.delete_kbd())
                # await state.set_state(Client.choose_super_power)
                # await query.message.edit_text(
                #     'Отлично, осталось совсем чуть-чуть🤏\nВыберите задачу, которую необходимо'
                #     'выполнить специалисту: ',
                #     reply_markup=await keyboards.get_abilities_ikb(query.data))
        else:
            await query.message.edit_text('Хорошо, но попробуй воспользоваться кнопками под сообщением....')
    except Exception as ex:
        print(f'Error in choose_spec menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.message(Client.add_new_specialty)
async def add_new_specialty(message: Message, state: FSMContext):
    await state.set_state(Client.choose_spec)
    await bot.send_message(chat_id=config.cv_id, text=f'Предложение новой специальности: {message.text}\n'
                                                      f'От пользователя: {message.from_user.id}')
    await message.answer(f'Замечательно мы постараемся добавить твою специальность: {message.text} в ближайшее время\n'
                         f'Пока можешь выбрать одну из меющихся специальностей:',
                         reply_markup=await keyboards.get_specialists_ikb())


# @router.callback_query(Client.choose_super_power)
# async def choose_super_power(query: CallbackQuery, state: FSMContext):
#     try:
#         spec = (await state.get_data()).get('choose_speс')
#         if query.data in config.abilities.get(spec):
#             await state.update_data(choose_super_power=query.data)
#             await state.set_state(Client.enter_descr)
#             await query.message.edit_text(text='Класс!\nОпишите суть задачи:',
#                                           reply_markup=await keyboards.delete_kbd())
#         else:
#             await query.message.edit_text('Хорошо, но попробуте воспользоваться кнопками под сообщением....')
#     except Exception as ex:
#         print(f'Error in choose_spec menu\n{ex}')
#         await query.message.answer(text=msg.errorMessage)


@router.message(Client.enter_descr)
async def enter_descr(message: Message, state: FSMContext):
    try:
        await state.update_data(enter_descr=message.text)
        await state.set_state(Client.enter_price)
        await message.answer(text='Замечательно!\nКакой бюджет вы готовы выделить(в BYN) на эту задачу?')
    except Exception as ex:
        print(f'Error in choose_spec menu\n{ex}')
        await message.answer(text=msg.errorMessage)


@router.message(Client.enter_price)
async def enter_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
        if price > 0:
            await state.update_data(enter_price=price)
            await state.set_state(Client.approve_project)
            info = await state.get_data()
            await message.answer(text='Почти закончили...\n'
                                      'Вот, что у вас получилось:\n\n'
                                      f'Название проекта: {info.get("enter_title")}\n'
                                      f'Необходимый специалист: {info.get("choose_speс")}\n'
                                      f'Описание задачи: {info.get("enter_descr")}\n'
                                      f'Бюджет: {price}BYN\n\n'
                                      f'Создать проект?', reply_markup=await keyboards.ask_create_project())
        else:
            await message.answer(text='Цена должна быть или целым или дусятичным неотрицательным числом!')
    except Exception as ex:
        print(f'Error in choose_spec menu\n{ex}')
        await message.answer(
            text=msg.errorMessage + '\nЦена должна быть или целым или дусятичным неотрицательным числом!')


@router.callback_query(and_f(Client.approve_project, or_f(QueryDataFilter('1'), QueryDataFilter('0'))))
async def approve_project(query: CallbackQuery, state: FSMContext):
    try:
        if int(query.data):
            sub_state = await db.if_user_can_create_project(query.from_user.id)
            if sub_state == -1:
                info = await state.get_data()
                order_id = await db.save_project(query.from_user.id, info.get("enter_title"), info.get("choose_speс"),
                                                 info.get("enter_descr"), info.get("enter_price"), -1)
                await query.message.edit_text(text=f'Ваш заказ #{order_id} сохранён, но для его размещения необходимо'
                                                   ' оформить подписку',
                                              reply_markup=await keyboards.buy_subscription())
            elif sub_state == 0:
                await query.message.edit_text(text='Для размещения проекта оформите подписку',
                                              reply_markup=await keyboards.buy_subscription())
            elif sub_state == 1:
                await query.message.edit_text(text='У вас уже создано максимальное число проектов\n'
                                                   'Чтобы создать новый удалите один из существующих'
                                                   ' или оформите подписку MAX',
                                              reply_markup=await keyboards.buy_subscription())
            elif sub_state == 2:
                info = await state.get_data()
                order_id = await db.save_project(query.from_user.id, info.get("enter_title"), info.get("choose_speс"),
                                                 info.get("enter_descr"), info.get("enter_price"), 0)
                await state.clear()
                await bot.send_message(chat_id=config.projects_id, text=f'{order_id}\n{query.from_user.id}\n\n'
                                                                        f'Название проекта: {info.get("enter_title")}\n'
                                                                        f'Необходимый специалист: {info.get("choose_speс")}\n'
                                                                        f'Описание задачи: {info.get("enter_descr")}\n'
                                                                        f'Бюджет: {info.get("enter_price")}BYN\n',
                                       reply_markup=await keyboards.accept_project_ikb())
                await query.message.edit_text(text=f'Отлично, ваш заказ #{order_id} отправлен на проверку!')
        else:
            await query.answer(text="Хорошо, заказ удалён!", cache_time=5)
            await state.clear()
            await state.set_state(Client.menu)
            await query.message.edit_text(text='Добро пожаловать в меню заказчика🧑‍💻',
                                          reply_markup=await keyboards.client_menu())
    except Exception as ex:
        print(f'Error in approve_project\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(QueryDataFilter('back'), or_f(Client.project_list, Client.choose_project)))
async def back_to_menu(query: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await state.set_state(Client.menu)
        await query.message.edit_text(text='Добро пожаловать в меню заказчика🧑‍💻',
                                      reply_markup=await keyboards.client_menu())
    except Exception as ex:
        print(f'Error in client_projects menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(QueryDataFilter('+1'), Client.choose_project))
async def next_project(query: CallbackQuery, state: FSMContext):
    try:
        projects = (await state.get_data()).get('projects_info')
        if projects[2] > 1:
            projects[1] += 1
            if projects[1] >= projects[2]:
                projects[1] = 0
            await state.update_data(projects_info=projects)
            await query.message.edit_text(
                text=await msg.display_project(projects[0][projects[1]], f'{projects[1] + 1}/{projects[2]}'),
                reply_markup=await keyboards.project_menu())
    except Exception as ex:
        print(f'Error in client_projects menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(QueryDataFilter('-1'), Client.choose_project))
async def previous_project(query: CallbackQuery, state: FSMContext):
    try:
        projects = (await state.get_data()).get('projects_info')
        if projects[2] > 1:
            projects[1] -= 1
            if projects[1] < 0:
                projects[1] = projects[2] - 1
            await state.update_data(projects_info=projects)
            await query.message.edit_text(
                text=await msg.display_project(projects[0][projects[1]], f'{projects[1] + 1}/{projects[2]}'),
                reply_markup=await keyboards.project_menu())
    except Exception as ex:
        print(f'Error in client_projects menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(QueryDataFilter('project_specialists'), Client.choose_project))
async def project_specialists(query: CallbackQuery, state: FSMContext):
    try:
        projects = (await state.get_data()).get('projects_info')
        specialists = await db.fetch_specialists(projects[0][projects[1]][3], query.from_user.id)
        print(specialists)
        if len(specialists) != 0:
            await state.update_data(specialists_info=[specialists, 0, len(specialists), projects[0][projects[1]]])
            await state.set_state(Client.choose_specialist)
            # await query.message.edit_text(text='Подходящие специалисты:', reply_markup=await keyboards.delete_kbd())
            await query.message.edit_text(text=await msg.display_specialists(specialists[0], f'{1}/{len(specialists)}'),
                                          reply_markup=await keyboards.specialists_list_menu())
        else:
            await query.answer(text=f'Подходящих спецалистов, пока не найдено(')
            # await asyncio.sleep(5)
    except Exception as ex:
        print(f'Error in client_projects menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(QueryDataFilter('delete'), Client.project_list))
async def delete_project(query: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        project_id = int(query.message.text.split('\n')[0][-4:])
        await state.update_data(delete_project_id=project_id)
        await state.set_state(Client.ask_delete_project)
        await query.message.edit_text(text=f'Вы хотите удалить проект #{project_id}?',
                                      reply_markup=await keyboards.delete_project_ikb())
    except Exception as ex:
        print(f'Error in client_projects menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(QueryDataFilter('+1'), Client.project_list))
async def next_project(query: CallbackQuery, state: FSMContext):
    try:
        projects = (await state.get_data()).get('projects_info')
        if projects[2] > 1:
            projects[1] += 1
            if projects[1] >= projects[2]:
                projects[1] = 0
            await state.update_data(projects_info=projects)
            await query.message.edit_text(
                text=await msg.display_project(projects[0][projects[1]], f'{projects[1] + 1}/{projects[2]}'),
                reply_markup=await keyboards.project_list())
    except Exception as ex:
        print(f'Error in client_projects menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(QueryDataFilter('-1'), Client.project_list))
async def previous_project(query: CallbackQuery, state: FSMContext):
    try:
        projects = (await state.get_data()).get('projects_info')
        if projects[2] > 1:
            projects[1] -= 1
            if projects[1] < 0:
                projects[1] = projects[2] - 1
            await state.update_data(projects_info=projects)
            await query.message.edit_text(
                text=await msg.display_project(projects[0][projects[1]], f'{projects[1] + 1}/{projects[2]}'),
                reply_markup=await keyboards.project_list())
    except Exception as ex:
        print(f'Error in client_projects menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(or_f(QueryDataFilter('1'), QueryDataFilter('0')), Client.ask_delete_project))
async def ask_delete_project(query: CallbackQuery, state: FSMContext):
    try:
        if int(query.data):
            if await db.delete_projects((await state.get_data()).get('delete_project_id')):
                await query.answer(text='Проект успешно удалён!', cache_time=3)
        await state.clear()
        await state.set_state(Client.menu)
        await query.message.edit_text(text='Добро пожаловать в меню заказчика🧑‍💻',
                                      reply_markup=await keyboards.client_menu())
    except Exception as ex:
        print(f'Error in client_projects menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(QueryDataFilter('back'), Client.choose_specialist))
async def back_to_projects(query: CallbackQuery, state: FSMContext):
    try:
        projects = (await state.get_data()).get('projects_info')
        if projects[2] > 1:
            await state.set_state(Client.choose_project)
            await state.update_data(projects_info=projects)
            await query.message.edit_text(
                text=await msg.display_project(projects[0][projects[1]], f'{projects[1] + 1}/{projects[2]}'),
                reply_markup=await keyboards.project_menu())
        else:
            await state.clear()
            await state.set_state(Client.menu)
            await query.message.edit_text(text='Добро пожаловать в меню заказчика🧑‍💻',
                                          reply_markup=await keyboards.client_menu())
    except Exception as ex:
        print(f'Error in client_projects menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(QueryDataFilter('+1'), Client.choose_specialist))
async def next_specialist(query: CallbackQuery, state: FSMContext):
    try:
        specialists = (await state.get_data()).get('specialists_info')
        if specialists[2] > 1:
            specialists[1] += 1
            if specialists[1] >= specialists[2]:
                specialists[1] = 0
            await state.update_data(specialists_info=specialists)
            await query.message.edit_text(
                text=await msg.display_specialists(specialists[0][specialists[1]],
                                                   f'{specialists[1] + 1}/{specialists[2]}'),
                reply_markup=await keyboards.specialists_list_menu())
    except Exception as ex:
        print(f'Error in client_projects menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(QueryDataFilter('-1'), Client.choose_specialist))
async def previous_specialist(query: CallbackQuery, state: FSMContext):
    try:
        specialists = (await state.get_data()).get('specialists_info')
        if specialists[2] > 1:
            specialists[1] -= 1
            if specialists[1] < 0:
                specialists[1] = specialists[2] - 1
            await state.update_data(specialists_info=specialists)
            await query.message.edit_text(
                text=await msg.display_specialists(specialists[0][specialists[1]],
                                                   f'{specialists[1] + 1}/{specialists[2]}'),
                reply_markup=await keyboards.specialists_list_menu())
    except Exception as ex:
        print(f'Error in client_projects menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(QueryDataFilter('choose_specialist'), Client.choose_specialist))
async def choose_specialist(query: CallbackQuery, state: FSMContext):
    try:
        specialists = (await state.get_data()).get('specialists_info')
        if await db.add_like(query.from_user.id, specialists[0][specialists[1]][0], specialists[3][1]):
            await bot.send_message(chat_id=specialists[0][specialists[1]][0], text=f'Вам пришло предложение работы!\n'
                                                                                   f'Проект #{specialists[3][1]}\n'
                                                                                   f'{await msg.display_offer_to_specialist(specialists[3])}',
                                   reply_markup=await keyboards.accept_offer_ikb())
            await query.answer(text='Предложение отправлено!')
            await state.clear()
            await state.set_state(Client.menu)
            await query.message.edit_text(text='Добро пожаловать в меню!', reply_markup=await keyboards.client_menu())
        else:
            await query.answer(text='Что-то пошло не так!')
            await asyncio.sleep(3)
    except Exception as ex:
        print(f'Error in client_projects menu\n{ex}')
        await query.message.answer(text=msg.errorMessage)
