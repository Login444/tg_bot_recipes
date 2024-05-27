import asyncio
import os

from dotenv import find_dotenv, load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# находим файл .env с помощью find_dotenv и загружаем переменные записанные в нем с помощью load_dotenv:
load_dotenv(find_dotenv())

from handlers.user_private import user_private_router
from common.bot_cmds_list import private

# создаем константу, в которою передадим список типов обновлений на которые должен реагировать бот:
ALLOWED_UPDATES = ["message", "edited_message"]

# Создаем класс бота, передаем в него токен, который предварительно выгрузили из файла .env:
bot = Bot(token=os.getenv('TOKEN'))

# создаем класс диспетчера, он будет обрабатывать все обновления для бота (команды, сообщения и т.д.):
dp = Dispatcher()

# добавляем в диспетчера роутеры которые мы создали в handlers
dp.include_routers(user_private_router)

# реализуем запуск бота в работу, он будет постоянно "слушать" сервер телеграм
# и спрашивать о наличии каких-либо обновлений для него - start:
async def main():
    """
    delete_webhook - сбрасывает ожидающие обновления, т.е. все обновления которые отправлялись пока бот был оффлайн
    start_polling - принимает все новые обновления с момента выхода бота в онлайн
    set_my_commands - настраивает команды которые будут добавлены в кнопку Menu, scope - указывает на тип чата,
    для которого доступны эти команды. Команды мы берем из common.bot_cmds_list.
    delet_my_commands - удаляет команды из кнопки Menu (если они заводились программно, то удалить их можно только так)
    """
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

# так как используем ассинхронное программирование, для запуска предыдущей функции используем следующую функцию:
asyncio.run(main())
