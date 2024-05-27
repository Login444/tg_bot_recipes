from aiogram.types import BotCommand

# формируем список команд, которые появятся в кнопке Menu для приватного чата:
private = [
    BotCommand(command='menu', description='Здесь будет появляться меню бота '
                                           '(добавить, посмотреть, редактировать, выбрать и т.д.)'),
    BotCommand(command='about', description='Тут появится подробное описание бота и его возможностей'),
    BotCommand(command='random', description='Тут будет запускаться рандомайзер рецептов'),
]