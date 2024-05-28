from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from filters.chat_types import ChatTypeFilter
from keyboards import reply
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup



# создаем роутер который будет обрабатывать события в личной переписке с пользователем
user_private_router = Router()
# вешаем на роутер наш собственный фильтр типа чата.
user_private_router.message.filter(ChatTypeFilter(['private']))


# создаем обработчик (handler) команды /start:
# При получении команды /start бот отправит в ответ сообщение о готовности к работе и стартовую клавиатуру,
# которую мы написали keyboards.reply
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет, я помогу тебе с выбором рецепта", reply_markup=reply.start_keyboard)


# В следующих обработчиках используем функуцию or_f(), в которую передаем два варианта сообщения:
# 1) команда меню формата /*
# 2) текст сообщения, который при помощи встроенного фильтра F мы приводим к нижнему регистру
# и сравниваем с указанным нами вариантом
# таким образом обработчик будет верно отрабатывать переданную команду, текст или сообщение,
# которое передает пользователь нажатием на кнопку из нашей клавиатуры


# создаем обработчик команды /menu
@user_private_router.message(or_f(Command('menu'), (F.text.lower() == 'меню')))
async def menu_cmd(message: types.Message):
    await message.answer( 'Добро пожаловать в меню. Выберите действие:',reply_markup=reply.main_menu_keyboard)


# создаем обработчик команды /about
@user_private_router.message(or_f(Command('about'), (F.text.lower() == 'о боте')))
async def about_cmd(message: types.Message):
    await message.answer("Тут появится подробное описание бота и его возможностей")


# создаем обработчик команды /random
@user_private_router.message(or_f(Command('random'), (F.text.lower() == 'случайный рецепт')))
async def random_cmd(message: types.Message):
    await message.answer("Тут будет запускаться рандомайзер рецептов")

# ниже пишу класс добавления рецепта для работы с машиной состояний (FSM)
class AddRecipe(StatesGroup):
    title = State()
    category = State()
    ingredients = State()
    cooking_time = State()
    steps = State()
    photo = State()



