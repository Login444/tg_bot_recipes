from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import String, Text, Integer, DateTime, func, ForeignKey, Column


class Base(DeclarativeBase):
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())



class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)



class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    ingredients = Column(String(500), nullable=False)
    cooking_time = Column(Integer, nullable=False)
    steps = Column(Text(1500), nullable=False)
    image = Column(String(150))
    author_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="recipes")
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", backref="recipes")
