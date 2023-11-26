# GENERAL KEYBOARDS:
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

import config


async def get_start_ikb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Работа✍', callback_data='looking_for_job'),
         InlineKeyboardButton(text='Специалисты👨‍💻', callback_data='looking_for_specialists')]
    ])


async def cancel_ikb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Отказаться', callback_data='cancel')]
    ])


async def delete_kbd():
    return None


async def get_specialists_ikb() -> InlineKeyboardMarkup:
    arr = []
    i = 0
    t = []
    for s in config.specialties:
        i += 1
        t.append(InlineKeyboardButton(text=s, callback_data=s))
        if i == 3:
            arr.append(t)
            t = []
            i = 0
    arr.append(t)
    return InlineKeyboardMarkup(inline_keyboard=arr)


async def get_abilities_ikb(spec: str) -> InlineKeyboardMarkup:
    arr = []
    i = 0
    t = []
    for s in config.abilities[spec]:
        i += 1
        t.append(InlineKeyboardButton(text=s, callback_data=s))
        if i == 3:
            arr.append(t)
            t = []
            i = 0
    arr.append(t)
    return InlineKeyboardMarkup(inline_keyboard=arr)


async def get_time_ikb() -> InlineKeyboardMarkup:
    arr = []
    i = 0
    t = []
    for s in config.times:
        i += 1
        t.append(InlineKeyboardButton(text=s, callback_data=s))
        if i == 3:
            arr.append(t)
            t = []
            i = 0
    arr.append(t)
    return InlineKeyboardMarkup(inline_keyboard=arr)


#
#
# WORKER KEYBOARDS
#
#
async def worker_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Моё резюме📄', callback_data='worker_cv'),
             InlineKeyboardButton(text='Поиск проекта🔍', callback_data='search_job')]
        ]
    )


async def cancel_enter_phone_ikb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Не вводить телефон', callback_data='cancel')]
    ])


async def get_worker_abilities_ikb(spec: str, bis=None) -> InlineKeyboardMarkup:
    if bis is None:
        bis = []
    arr = []
    i = 0
    t = []
    for s in config.abilities[spec]:
        if s not in bis:
            i += 1
            t.append(InlineKeyboardButton(text=s, callback_data=s))
            if i == 3:
                arr.append(t)
                t = []
                i = 0
    if len(bis) != 0:
        t.append(InlineKeyboardButton(text='Больше нет😉', callback_data='stop'))
    arr.append(t)
    return InlineKeyboardMarkup(inline_keyboard=arr)


async def check_cv_ikb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Сохранить💾', callback_data='1'),
         InlineKeyboardButton(text='Не сохранять', callback_data='0')]
    ])


async def ask_to_edit_cv_ikb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Изменить⚙️', callback_data='change_cv'),
         InlineKeyboardButton(text='Не изменять❌', callback_data='cancel_change_cv')]
    ])


async def worker_menu_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Меню разработчика', callback_data='looking_for_job')]
        ]
    )


async def accept_offer_ikb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Откликнуться👋', callback_data='reply_to_offer'),
         InlineKeyboardButton(text='Отклонить❌', callback_data='decline_offer')]
    ])


async def afk_ikb(b) -> InlineKeyboardMarkup:
    if b:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Не хочу🚫', callback_data='0')]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Хочу получать📩', callback_data='1')]
            ]
        )


#
#
# CLIENT KEYBOARDS
#
#
async def client_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Мои проекты📋', callback_data='client_projects'),
             InlineKeyboardButton(text='Создать проект🛠', callback_data='create_project')],
            [InlineKeyboardButton(text='Поиск специалистов🔎', callback_data='search_spec')]
        ]
    )


async def client_menu_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Меню заказчика', callback_data='looking_for_specialists')]
        ]
    )


async def ask_create_project() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Создать🆕', callback_data='1'),
             InlineKeyboardButton(text='Не создавать❌', callback_data='0')]
        ]
    )


async def ask_buy_max() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Оформить✍️', callback_data='buy_max'),
             InlineKeyboardButton(text='Не оформлять', callback_data='cancel')]
        ]
    )


async def buy_subscription() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Оформить✍️', callback_data='buy_subscription')]
        ]
    )


async def choose_project() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Оформить✍️', callback_data='buy_subscription')]
        ]
    )


async def project_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='<', callback_data='-1'),
             InlineKeyboardButton(text='>', callback_data='+1')],
            [InlineKeyboardButton(text='Специалисты🔎', callback_data='project_specialists')],
            [InlineKeyboardButton(text='Назад🔙', callback_data='back')]
        ]
    )


async def project_list() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='<', callback_data='-1'),
             InlineKeyboardButton(text='>', callback_data='+1')],
            [InlineKeyboardButton(text='Удалить проект🗑', callback_data='delete')],
            [InlineKeyboardButton(text='Назад🔙', callback_data='back')]
        ]
    )


async def delete_project_ikb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Да', callback_data='1'),
             InlineKeyboardButton(text='Нет', callback_data='0')]
        ]
    )


async def specialists_list_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='<', callback_data='-1'),
             InlineKeyboardButton(text='>', callback_data='+1')],
            [InlineKeyboardButton(text='Выбрать✅', callback_data='choose_specialist')],
            [InlineKeyboardButton(text='Назад🔙', callback_data='back')]
        ]
    )


#
#
# ADMINS KEYBOARDS
#
#
async def accept_project_ikb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Принять', callback_data='accept_project'),
             InlineKeyboardButton(text='Отклонить', callback_data='decline_project')]
        ]
    )


async def accept_cv_ikb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Принять', callback_data='accept_cv'),
             InlineKeyboardButton(text='Отклонить', callback_data='decline_cv')]
        ]
    )
