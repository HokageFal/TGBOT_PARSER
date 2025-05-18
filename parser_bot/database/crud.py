from datetime import datetime
from http.client import HTTPException

from sqlalchemy import select, insert, delete
from parser_bot.database.models import User, Skill


async def get_user(session, telegram_id: int, username: int):
    result = await session.execute(select(User).filter(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()

    if not user:
        user = await session.execute(insert(User).values(
            telegram_id=telegram_id, username=username, created_at=datetime.utcnow()
        ))
        await session.commit()

    return user

async def get_skills(session, telegram_id: int, skills: list) -> list:
    await session.execute(
        delete(Skill).where(Skill.user_id == telegram_id)
    )
    new_skill = []
    for i in skills:
        await session.execute(insert(Skill).values(
            user_id=telegram_id, title=i
        ))
        new_skill.append(i)
    await session.commit()

    return new_skill