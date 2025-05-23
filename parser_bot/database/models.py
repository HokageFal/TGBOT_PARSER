from datetime import datetime
from sqlalchemy import ForeignKey, String, Text, Integer, Table, Column
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from parser_bot.database.core import Base

# Определяем ассоциативную таблицу для связи многие-ко-многим
user_skill_association = Table(
    'user_skills',
    Base.metadata,
    Column('user_id', ForeignKey('users.telegram_id'), primary_key=True),
    Column('skill_id', ForeignKey('skills.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(50))
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Связь многие-ко-многим с навыками через ассоциативную таблицу
    skills: Mapped[list["Skill"]] = relationship(
        secondary=user_skill_association,
        back_populates="users"
    )


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    title: Mapped[str] = mapped_column(String(255), unique=True)

    # Связь с пользователями
    users: Mapped[list["User"]] = relationship(
        secondary=user_skill_association,
        back_populates="skills"
    )

    # Связь с вопросами (один-ко-многим)
    questions: Mapped[list["Question"]] = relationship(
        back_populates="skill",
        cascade="all, delete-orphan"
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    text: Mapped[str] = mapped_column(Text)

    # Связь с навыком
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    skill: Mapped["Skill"] = relationship(back_populates="questions")