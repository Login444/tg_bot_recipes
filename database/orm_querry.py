from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Recipe, Category, User
from sqlalchemy import select, update, delete


async def orm_add_recipe(session: AsyncSession, data: dict):
    """
    функция осуществляет запись рецепта в БД

    :param session: - объект сессии
    :param data: - словарь с данными полученными в результате заполнения в FSM
    """
    # здесь делается запрось к таблице категорий, если такое название категории уже существует, то в рецепт записывается
    # уже существующая категория, в противном случае создается новая запись в таблице категорий
    category_query = select(Category).where(Category.title == data['category'])
    cat_exec = await session.execute(category_query)
    existing_category = cat_exec.scalars().first()
    if existing_category is None:
        category = Category(title=data['category'])
        session.add(category)
    else:
        category = existing_category

    # аналогичный алгоритм с проверкой на существующего пользователя
    user_query = select(User).where(User.user_id == data['user_id'])
    user_exec = await session.execute(user_query)
    existing_user = user_exec.scalars().first()
    if existing_user is None:
        user = User(user_id=data['user_id'])
        session.add(user)
    else:
        user = existing_user

    # создаем класс рецепта, все значения берем из словаря переданного в аргумент функции
    recipe = Recipe(
        title=data['title'],
        ingredients=data['ingredients'],
        cooking_time=data['cooking_time'],
        steps=data['steps'],
        image=data['photo'],
        category=category,
        user=user
    )

    session.add(recipe)
    await session.commit()


