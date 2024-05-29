from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, Integer


class Base(DeclarativeBase):
    pass


class Recipe(Base):
    __tablename__ = 'recipe'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str]
    ingridients: Mapped[str] = mapped_column(String(500), nullable=False)
    cooking_time: Mapped[int] = mapped_column(Integer(), nullable=False)
    steps: Mapped[str] = mapped_column(Text(1500), nullable=False)
    image: Mapped[str] = mapped_column(String(150))