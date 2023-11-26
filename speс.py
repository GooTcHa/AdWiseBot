from aiogram import Router, F
from aiogram.filters import and_f, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import config
import db
import keyboards
import msg
from filters import QueryDataFilter
from states import User, Worker

import main

router = Router(name=__name__)


@router.callback_query(QueryDataFilter('looking_for_job'))
async def user_looking_for_job(query: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await state.set_state(Worker.menu)
        await query.message.edit_text(text='Меню специалиста🏢', reply_markup=await keyboards.worker_menu())
    except Exception as ex:
        print(ex, type(ex))


@router.callback_query(QueryDataFilter('reply_to_offer'))
async def reply_to_offer(query: CallbackQuery, state: FSMContext):
    try:
        project_id = query.message.text.split('\n')[1][-4:]
        client_id = await db.reply_to_offer(project_id)
        spec_info = await db.get_specialist_info(query.from_user.id)
        if spec_info[6] != 'None':
            await main.bot.send_message(chat_id=client_id, text=f'Пользователь откликнулся на ваше предложение'
                                                                f' по заказу #{project_id}\n\nИмя: {spec_info[4]}\n'
                                                                f'Специальность: {spec_info[8]}\nTelegram: {spec_info[2]}\n'
                                                                f'Email: {spec_info[5]}\nPhone: {spec_info[6]}')
        else:
            await main.bot.send_message(chat_id=client_id, text=f'Пользователь откликнулся на ваше предложение'
                                                                f' по заказу #{project_id}\n\nИмя: {spec_info[4]}\n'
                                                                f'Специальность: {spec_info[8]}\nTelegram: {spec_info[2]}\n'
                                                                f'Email: {spec_info[5]}\n')
        await query.message.edit_text(text='Заказчику были отправлены ваши контактные данные!\n'
                                           'В скором времени он с вами свяжется')
        await query.answer(text='Ответ отправлен!')
    except Exception as ex:
        print(ex)
        await query.message.edit_text(text='Извините, но предложение уже не активно(')


@router.callback_query(QueryDataFilter('worker_cv'))
async def edit_cv(query: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        info = await db.get_user_cv(query.from_user.id)
        print(info)
        if info is not None and not info[7]:
            await query.message.edit_text(text=f'Ваше резюме находиться на рассмотрении!',
                                          reply_markup=await keyboards.delete_kbd())
        elif info is not None:
            cv_info = info
            print(cv_info)
            # skills = cv_info[1]
            if cv_info[3] != 'None':
                await query.message.edit_text(text=f'Ваше резюме:\n\nВаше имя: {cv_info[1]}\n'
                                                   f'email: {cv_info[2]}\nТелефой: {cv_info[3]}\n'
                                                   f'Портфолио: {cv_info[4]}\nСпециализация: {cv_info[5]}\n'
                                                   f'Хотите его изменить?',
                                              reply_markup=await keyboards.ask_to_edit_cv_ikb())
            else:
                await query.message.edit_text(text=f'Ваше резюме:\n\nВаше имя: {cv_info[1]}\n'
                                                   f'email: {cv_info[2]}\n'
                                                   f'Портфолио: {cv_info[4]}\nСпециализация: {cv_info[5]}\n'
                                                   f'Хотите его изменить?',
                                              reply_markup=await keyboards.ask_to_edit_cv_ikb())
            await state.set_state(Worker.look_through_cvs)

        else:
            await query.message.edit_text(text='У вас пока нет резюме\nДавайте начнём его заполнение'
                                               '\nВведите ваше имя:',
                                          reply_markup=await keyboards.delete_kbd())
            await state.set_state(Worker.enter_name)
    except Exception as ex:
        print(f'Error in spec.search_job\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(QueryDataFilter('change_cv'), Worker.look_through_cvs))
async def edit_cv(query: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await query.message.edit_text(text='Давайте начнём заполнение'
                                           '\nВведите ваше имя:',
                                      reply_markup=await keyboards.delete_kbd())
        await state.set_state(Worker.enter_name)
    except Exception as ex:
        print(f'Error in spec.search_job\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(QueryDataFilter('cancel_change_cv'), Worker.look_through_cvs))
async def cancel_change_cv(query: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await state.set_state(Worker.menu)
        await query.message.edit_text(text='Меню специалиста🏢', reply_markup=await keyboards.worker_menu())
    except Exception as ex:
        print(f'Error in spec.search_job\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(QueryDataFilter('search_job'))
async def search_job(query: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        if await db.check_cv(query.from_user.id):
            # print(await db.if_user_afk(query.from_user.id))
            b = await db.if_user_afk(query.from_user.id)
            if b != -1:
                await query.message.edit_text(text='Хотите ли получать новые предложения о работе?',
                                              reply_markup=await keyboards.afk_ikb(b))
                await state.set_state(Worker.switch_afk)
            else:
                await state.clear()
                await query.message.edit_text(text='Ваше резюме находиться на рассмотрении...',
                                              reply_markup=await keyboards.worker_menu())
        else:
            await query.message.edit_text(text='У вас не заполнено резюме!\nДавайте начнём его заполнение'
                                               '\nВведите ваше имя:',
                                          reply_markup=await keyboards.delete_kbd())
            await state.set_state(Worker.enter_name)
    except Exception as ex:
        print(f'Error in spec.search_job\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.callback_query(and_f(or_f(QueryDataFilter('0'), QueryDataFilter('1')), Worker.switch_afk))
async def switch_afk(query: CallbackQuery, state: FSMContext):
    try:
        if await db.switch_afk(query.from_user.id, int(query.data)):
            if int(query.data) == 0:
                await query.answer(text='Поиск успешно отключён!', cache_time=3)
            else:
                await query.answer(text='Поиск успешно включён!', cache_time=3)
            await state.set_state(Worker.menu)
            await query.message.edit_text(text='Меню специалиста🏢', reply_markup=await keyboards.worker_menu())
    except Exception as ex:
        print(f'Error in spec.search_job\n{ex}')
        await query.message.answer(text=msg.errorMessage)


@router.message(Worker.enter_name)
async def enter_name(message: Message, state: FSMContext):
    try:
        await state.update_data(enter_name=message.text)
        await state.set_state(Worker.enter_email)
        await message.answer(text='Отлично😉\nИдём дальше\nВведите адрес вашей электронной почты:',
                             reply_markup=await keyboards.delete_kbd())
    except Exception as ex:
        print(f'Exceptinon in ener_name:\n{ex}')


@router.message(and_f(F.text.contains('@'), Worker.enter_email))
async def enter_email(message: Message, state: FSMContext):
    try:
        await state.update_data(enter_email=message.text)
        await state.set_state(Worker.enter_phone)
        await message.answer(text='Введите номер телефона:',
                             reply_markup=await keyboards.cancel_enter_phone_ikb())
    except Exception as ex:
        print(f'Exceptinon in ener_name:\n{ex}')


@router.message(Worker.enter_email)
async def enter_wrong_email(message: Message, state: FSMContext):
    try:
        await message.answer(text='Неверный формат ввода!\nАдрес почты должен содержать @ в названии')
    except Exception as ex:
        print(f'Exceptinon in ener_wrong_name:\n{ex}')


@router.message(and_f(F.text.contains('+375'), Worker.enter_phone))
async def enter_phone(message: Message, state: FSMContext):
    try:
        if len(message.text) == 13:
            await state.update_data(enter_phone=message.text)
            await state.set_state(Worker.choose_specialty)
            await message.answer(text='Замечательно!\nТеперь выберите свою специальность:',
                                 reply_markup=await keyboards.get_specialists_ikb())
        else:
            await message.answer(text='Неверный формат ввода номера!\nВведите номер в формате: +375XXXXXXXXX',
                                 reply_markup=await keyboards.cancel_enter_phone_ikb())
    except Exception as ex:
        print(f'Exceptinon in ener_name:\n{ex}')


@router.message(Worker.enter_phone)
async def enter_wrong_phone(message: Message, state: FSMContext):
    try:
        await message.answer(text='Неверный формат ввода номера!\n'
                                  'Необходимо использовать белорусский номер с кодом +375',
                             reply_markup=await keyboards.cancel_enter_phone_ikb())
    except Exception as ex:
        print(f'Exceptinon in ener_name:\n{ex}')


@router.callback_query(and_f(Worker.enter_phone, QueryDataFilter('cancel')))
async def enter_email(query: CallbackQuery, state: FSMContext):
    try:
        await state.update_data(enter_phone=None)
        await state.set_state(Worker.choose_specialty)
        await query.message.edit_text(text='Вас понял!\nВыберите свою специальность:',
                                      reply_markup=await keyboards.get_specialists_ikb())
    except Exception as ex:
        print(f'Exceptinon in ener_name:\n{ex}')


@router.callback_query(Worker.choose_specialty)
async def choose_specialty(query: CallbackQuery, state: FSMContext):
    try:
        if query.data in config.specialties:
            if query.data == config.specialties[-1]:
                await state.set_state(Worker.add_new_specialty)
                await query.message.edit_text('Введи название своей специализации и мы добавим её в ближайшем времени:',
                                              reply_markup=await keyboards.delete_kbd())
            else:
                await state.update_data(choose_specialty=query.data)
                await state.set_state(Worker.enter_link)
                await query.message.edit_text(text='Введите ссылку на ваше портфолио:',
                                              reply_markup=await keyboards.delete_kbd())
                # await state.set_state(Worker.choose_super_power)
                #
                # await query.message.edit_text('Отлично, осталось совсем чуть-чуть🤏\nВыбери свои суперспособности: ',
                #                               reply_markup=await keyboards.get_worker_abilities_ikb(query.data))
                # TODO суперспособности
        else:
            await query.message.edit_text('Хорошо, но попробуй воспользоваться кнопками под сообщением....')
    except Exception as ex:
        print(f'Exceptinon in ener_name:\n{ex}')


@router.message(Worker.enter_link)
async def enter_link(message: Message, state: FSMContext):
    try:
        await state.update_data(enter_link=message.text)
        await state.set_state(Worker.check_cv)
        info = await state.get_data()
        await message.answer(text=f'Отлично!\nВот, что у вас получилось:\nВаше имя:{info.get("enter_name")}\n'
                                  f'Ваша специальность: {info.get("choose_specialty")}\n'
                                  f'Ссылка на ваше портфолио: {info.get("enter_link")}\n'
                                  f'Номер телефона: {info.get("enter_phone")}\n'
                                  f'Email: {info.get("enter_email")}\n\n'
                                  f'Сохранить резюме?',
                             reply_markup=await keyboards.check_cv_ikb())
    except Exception as ex:
        print(f'Exceptinon in ener_link: {ex}')


# @router.callback_query(and_f(Worker.choose_super_power, QueryDataFilter('stop')))
# async def stop_choose_super_power(query: CallbackQuery, state: FSMContext):
#     try:
#         await state.set_state(Worker.check_cv)
#         info = await state.get_data()
#         abil = ''
#         for a, t in zip(info.get('choose_super_power')[:-1], info.get('choose_duration')[:-1]):
#             abil += f'{a} - {t},\n'
#         abil += f'{info.get("choose_super_power")[-1]} - {info.get("choose_duration")[-1]}'
#         await query.message.edit_text(text=f'Отлично!\nВот, что у вас получилось:\nВаше имя:{info.get("enter_name")}\n'
#                                            f'Ваша специальность: {info.get("choose_specialty")}\n'
#                                            f'Ссылка на ваше портфолио: {info.get("enter_link")}\n'
#                                            f'Навыки: {abil}\n'
#                                            f'Номер телефона: {info.get("enter_phone")}\n'
#                                            f'Email: {info.get("enter_email")}\n\n'
#                                            f'Сохранить резюме?',
#                                       reply_markup=await keyboards.check_cv_ikb())
#
#     except Exception as ex:
#         print(f'Exceptinon in ener_name:\n{ex}')


# @router.callback_query(Worker.choose_super_power)
# async def choose_super_power(query: CallbackQuery, state: FSMContext):
#     try:
#         spec = (await state.get_data()).get('choose_specialty')
#         if query.data in config.abilities[spec]:
#             info = await state.get_data()
#             arr = []
#             if 'choose_super_power' in info.keys():
#                 arr = info.get('choose_super_power')
#                 arr.append(query.data)
#                 await state.update_data(choose_super_power=arr)
#             else:
#                 arr.append(query.data)
#                 await state.update_data(choose_super_power=arr)
#             await state.set_state(Worker.choose_duration)
#             await query.message.edit_text(text='Укажите среднее время, затрачиваемое на задачу:',
#                                           reply_markup=await keyboards.get_time_ikb())
#         else:
#             pass
#             # TODO else case
#
#     except Exception as ex:
#         print(f'Exceptinon in choose_super_power:\n{ex}')
#
#
# @router.callback_query(Worker.choose_duration)
# async def choose_duration(query: CallbackQuery, state: FSMContext):
#     try:
#         if query.data in config.times:
#             arr = []
#             if 'choose_duration' in (await state.get_data()).keys():
#                 arr = (await state.get_data()).get('choose_duration')
#             arr.append(query.data)
#             await state.update_data(choose_duration=arr)
#             await state.set_state(Worker.choose_super_power)
#             arr = (await state.get_data()).get('choose_super_power')
#             spec = (await state.get_data()).get('choose_specialty')
#             await query.message.edit_text(text='Отлично👍\nЕсть ещё?',
#                                           reply_markup=await keyboards.get_worker_abilities_ikb(spec, arr))
#         else:
#             # TODO else case
#             pass
#
#     except Exception as ex:
#         print(f'Exceptinon in choose_duration:\n{ex}')


@router.callback_query(Worker.check_cv)
async def check_cv(query: CallbackQuery, state: FSMContext):
    try:
        if int(query.data):
            info = await state.get_data()
            if await db.save_cv(query.from_user.id, info.get("enter_name"), info.get("enter_email"),
                                info.get("enter_phone"),
                                info.get('enter_link'),
                                info.get("choose_specialty")):
                await main.bot.send_message(chat_id=config.cv_id, text=f'{query.from_user.id}\n\nРезюме\n\n'
                                                                                  f'Имя: {info.get("enter_name")}\n'
                                                                                  f'Ваша специальность: {info.get("choose_specialty")}\n'
                                                                                  f'Ссылка на ваше портфолио: {info.get("enter_link")}\n'
                                                                                  f'Номер телефона: {info.get("enter_phone")}\n'
                                                                                  f'Email: {info.get("enter_email")}',
                                            reply_markup=await keyboards.accept_cv_ikb())
                await state.clear()
                await query.message.edit_text(text=f'Резюме отправлено на проверку!',
                                              reply_markup=await keyboards.delete_kbd())
        else:
            # TODO else case
            pass

    except Exception as ex:
        print(f'Exceptinon in check_cv:\n{ex}')


@router.message(Worker.add_new_specialty)
async def add_new_specialty(message: Message, state: FSMContext):
    await state.set_state(Worker.choose_specialty)
    await main.bot.send_message(chat_id=config.cv_id, text=f'Предложение новой специальности: {message.text}\n'
                                                           f'От пользователя: {message.from_user.id}')
    await message.answer(f'Замечательно мы постараемся добавить твою специальность: {message.text} в ближайшее время\n'
                         f'Пока можешь выбрать одну из меющихся специальностей:',
                         reply_markup=await keyboards.get_specialists_ikb())
