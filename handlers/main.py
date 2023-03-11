from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
# from data_base import sqlite_db
from aiogram.dispatcher.filters import Text

from get_data import get_data
from get_table import get_table

ID = None



class FSMAdmin(StatesGroup):
    topic = State()
    min_difficulty = State()
    max_difficulty = State()


# Начало работы загруки пункта меню
# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    await FSMAdmin.topic.set()
    await bot.send_message(message.from_user.id, 'Введите тему задания')


# Ловим первый ответ пользователя
# @dp.message_handler(commands=['photo'], state=FSMAdmin.photo)
async def load_topic(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['topic'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, "Введите минимальный порог сложности")


# Ловим второй ответ пользователя
# @dp.message_handler(state=FSMAdmin.name)
async def load_min_difficulty(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['min_difficulty'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, "Введите максимальный порог сложности")


# @dp.message_handler(state=FSMAdmin.price)
async def load_max_difficulty(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['max_difficulty'] = message.text
    # await sqlite_db.sql_add_command(state)
    await bot.send_message(message.from_user.id, "Принято, подготавливаю задачи")
    if int(data['min_difficulty']) < int(data['max_difficulty']):
        data_tusk = get_data(data['topic'], data['min_difficulty'], data['max_difficulty'])
    else:
        data_tusk = get_data(data['topic'], data['max_difficulty'], data['min_difficulty'])
    if not bool(data_tusk):
        await bot.send_message(message.from_user.id, "Таких задач нет")
    else:
        table = get_table(data_tusk)
        await bot.send_message(message.from_user.id, table)
    await state.finish()


@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Задачи'])
    dp.register_message_handler(load_topic, state=FSMAdmin.topic)
    dp.register_message_handler(load_min_difficulty, state=FSMAdmin.min_difficulty)
    dp.register_message_handler(load_max_difficulty, state=FSMAdmin.max_difficulty)
    dp.register_message_handler(cancel, state="*", commands='отмена')
    dp.register_message_handler(cancel, Text(equals='отмена', ignore_case=True), state='*')
