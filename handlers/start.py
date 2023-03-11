from aiogram import types, Dispatcher

from create_bot import bot
from keybords import kb_button


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Добрый день!', reply_markup=kb_button)
    await message.delete()


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
