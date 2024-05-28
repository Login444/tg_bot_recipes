from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# пишем стартовую клавиатуру (кнопки которые будут доступны при старте работы с ботом)
# для этого создаем экземпляр класса ReplyKeyboardMarkup,
# в который передаем список списков кнопок (экземпляры класса KeyboardButton)
# каждый список, это отдельный ряд кнопок.
# что бы кнопки приняли правильный размер, используем параметр resize_keyboard
# параметр input_field_placeholder используем что бы изменить текст в строке ввода

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Меню'),
            KeyboardButton(text='О боте'),
        ],
        [
            KeyboardButton(text='Случайный рецепт'),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Что Вас интересует?'
)

# создаем переменную для удаления имеющейся клавиатуры.
# Далее мы сможем так же передавать его в обработчиках в аргументе reply_markup
delete_keyboard = ReplyKeyboardRemove()

# напишем клавиатуру для основного меню бота
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Категории рецептов'),
            KeyboardButton(text='Мои рецепты'),
        ],
        [
            KeyboardButton(text='Добавить свой рецепт'),
            KeyboardButton(text='Редактировать свой рецепт'),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Что Вас интересует?'
)

# add_recipe_keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text='Добавить название'),
#             KeyboardButton(text='Добавить категорию'),
#             KeyboardButton(text='Добавить ингридиенты'),
#         ],
#         [
#             KeyboardButton(text='Добавить время приготовления'),
#             KeyboardButton(text='Шаги приготовления'),
#             KeyboardButton(text='Добавить фото блюда'),
#         ],
#     ],
# )