from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from filters.chat_types import ChatTypeFilter
from keyboards import reply
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_querry import orm_add_recipe, orm_add_user, orm_add_category

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
    await message.answer('Добро пожаловать в меню. Выберите действие:', reply_markup=reply.main_menu_keyboard)


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

    texts = {
        'AddRecipe:title': 'Введите название заново',
        'AddRecipe:category': 'Введите категорию заново',
        'AddRecipe:ingredients': 'Введите ингридиенты заново',
        'AddRecipe:cooking_time': 'Введите время приготовления заново заново',
        'AddRecipe:steps': 'Введите шаги приготовления заново',
        'AddRecipe:photo': 'Прикрепите фото заново'
    }


# ниже код для машины состояний (FSM)
@user_private_router.message(StateFilter(None), F.text == "Добавить свой рецепт")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название блюда", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddRecipe.title)


@user_private_router.message(AddRecipe.title, F.text)
async def add_product(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text, user_id=message.from_user.id)
    await message.answer("Введите категорию блюда")
    await state.set_state(AddRecipe.category)


@user_private_router.message(AddRecipe.title)
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели неверные данные, напишите назавние блюда")


@user_private_router.message(AddRecipe.category, F.text)
async def add_product(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text.capitalize())
    await message.answer("Укажите все ингридиенты")
    await state.set_state(AddRecipe.ingredients)


@user_private_router.message(AddRecipe.category)
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели неверные данные, напишите категорию блюда")


@user_private_router.message(AddRecipe.ingredients, F.text)
async def add_product(message: types.Message, state: FSMContext):
    await state.update_data(ingredients=message.text)
    await message.answer("Укажите время приготовления в минутах")
    await state.set_state(AddRecipe.cooking_time)


@user_private_router.message(AddRecipe.ingredients)
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели неверные данные, напишите ингридиенты блюда")


@user_private_router.message(AddRecipe.cooking_time, F.text)
async def add_product(message: types.Message, state: FSMContext):
    await state.update_data(cooking_time=message.text)
    await message.answer("Опишите шаги приготовления")
    await state.set_state(AddRecipe.steps)


@user_private_router.message(AddRecipe.cooking_time)
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели неверные данные, напишите время приготовления блюда")


@user_private_router.message(AddRecipe.steps, F.text)
async def add_product(message: types.Message, state: FSMContext):
    await state.update_data(steps=message.text)
    await message.answer("Прикерпеите фото блюда")
    await state.set_state(AddRecipe.photo)


@user_private_router.message(AddRecipe.steps)
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели неверные данные, напишите шаги приготовления блюда")


@user_private_router.message(AddRecipe.photo, F.photo)
async def add_product(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()
    # try:
    await orm_add_recipe(session, data=data)
    await message.answer("Рецепт добавлен", reply_markup=reply.main_menu_keyboard)
    await state.clear()
    # except Exception as e:
    #     await message.answer('Что то пошло не так, попробуйте позже', reply_markup=reply.main_menu_keyboard)
    #     await state.clear()


@user_private_router.message(AddRecipe.photo)
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели неверные данные, прикрепите фото блюда")


@user_private_router.message(StateFilter('*'), Command("Отмена"))
@user_private_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_cmd(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Действия отменены", reply_markup=reply.main_menu_keyboard)


@user_private_router.message(StateFilter('*'), Command("Назад"))
@user_private_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_cmd(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is AddRecipe.title:
        await message.answer('Предыдущего шага нет, напишите "отмена" либо введите назавние блюда')
        return
    previous = None
    for step in AddRecipe.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f'Вы вернулись к предыдущему шагу \n {AddRecipe.texts[previous.state]}')
            return
        previous = step
