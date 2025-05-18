from codecs import backslashreplace_errors
from collections.abc import Mapping
from datetime import datetime
from sqlalchemy import ForeignKey, String, Text, Boolean, DateTime, Integer
from parser_bot.database.core import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime]

    skills: Mapped[List["Skill"]] = relationship()

class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    title: Mapped[str] = mapped_column(String(255), unique=True)