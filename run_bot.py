import multiprocessing
from aiogram.utils import executor
from create_bot import dp, bot
from run_script_pars import function_write_data
from handlers import start, main


async def on_startup(_):
    multiprocessing.Process(target=function_write_data).start()
    print('Бот вышел в онлайн')
    print('Запущен скрипт, который будет обновлять данные в БД каждый час')


if __name__ == '__main__':
    main.register_handlers_main(dp)
    start.register_handlers_start(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
