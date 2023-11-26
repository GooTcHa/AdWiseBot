import datetime

from aiogram.utils.markdown import hbold

errorMessage = 'Упс... Что-то пошло не так....\nПопробуйте ещё раз'


async def start_message(user_name) -> str:
    return f'Привет {hbold(user_name)}.\nДай угадаю.\n' \
           f'Ты здесь, потому что  ты ищешь крутого специалиста в команду или ты и есть тот самый крутой специалист ' \
           f'способный решить любую задачу бизнеса?\n' \
           f'Этот бот, всего в несколько кликов решит проблему кем ты не был и какая бы сложная задача перед тобой ' \
           f'не стояла.\n' \
           f'Пока ты это читал, мы уже начали анализировать твой запрос и подбирать для тебя лучшие варианты ' \
           f'заказчиков и исполнителей.\n\n' \
           f'Хватит уже залипать в экран. Кликай, покажем что мы умеем)'


async def display_project(project, it) -> str:
    return f'#{project[1]}\n\nНазвание: {project[2]}\nСпециалист: {project[3]}\n' \
           f'Описание: {project[4]}\nПердложение: {project[5]}BYN\nСрок истечения: {project[6].date()}\n\n{it}'


async def display_specialists(specialist, it) -> str:
    return f'Имя: {specialist[1]}\nСпециальность: {specialist[5]}\n' \
           f'Ссылка на портфолио: {specialist[4]}\n\n{it}'


async def display_offer_to_specialist(project) -> str:
    return f'Название: {project[2]}\nТребуемый специалист: {project[3]}\nТребуемый скилл: {project[4]}\n' \
           f'Описание задачи: {project[5]}\nПердложение: {project[6]}BYN'
