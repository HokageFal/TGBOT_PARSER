from datetime import datetime
from http.client import HTTPException
from typing import Optional
from sqlalchemy import select, insert, delete, func
from parser_bot.database.models import User, Skill, Question, user_skill_association

async def get_user(session, telegram_id: int, username: str):
    result = await session.execute(select(User).filter(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()

    if not user:
        user = await session.execute(insert(User).values(
            telegram_id=telegram_id, username=username, created_at=datetime.utcnow()
        ))
        await session.commit()

    return user

async def add_skills(session, telegram_id: int, skills: list, username: str) -> list:
    skills = set(skills)
    new_skill = []
    for i in skills:
        result = await session.execute(select(Skill).where(Skill.title == i))
        skill = result.scalars().first()

        if not skill:
            await session.execute(insert(Skill).values(
                title=i
            ))

            await session.flush()

            result = await session.execute(select(Skill).where(Skill.title == i))
            skill = result.scalars().first()

        user = await get_user(session, telegram_id, username)
        result = await session.execute(
            select(user_skill_association)
            .where(
                user_skill_association.c.user_id == user.telegram_id,
                user_skill_association.c.skill_id == skill.id
            )
        )

        if not result.first():
            await session.execute(
                user_skill_association.insert()
                .values(user_id=user.telegram_id, skill_id=skill.id)
            )


        new_skill.append(i)

    await session.commit()

    return new_skill

async def get_skills(session, telegram_id: int) -> list:
    result = await session.execute(select(Skill.title).
                                   join(user_skill_association,
                                        Skill.id == user_skill_association.c.skill_id).
                                   filter(user_skill_association.c.user_id==telegram_id))
    skills = result.scalars().all()

    return skills

async def delete_skill(session, telegram_id: int, skill_name: str):
    skill_id = await session.execute(select(Skill.id).filter(Skill.title==skill_name))
    skill_id = skill_id.scalars().first()

    if not skill_id:
        raise ValueError("Нот фоунд")

    await session.execute(delete(user_skill_association).filter(
        user_skill_association.c.skill_id==skill_id, user_skill_association.c.user_id==telegram_id))

    await session.commit()

    return {"message": "Навык удален"}

async def add_skill(session, telegram_id: int, title: str):
    result = await session.execute(select(Skill.id).where(Skill.title == title))
    skill_id = result.scalars().first()

    await session.execute(insert(user_skill_association).values(
        user_id=telegram_id, skill_id=skill_id
    ))

    await session.commit()

    return {"message": "Успешно добавлено"}

async def get_question_for_skills(session, skill_title: str):
    skill = await session.execute(select(Skill).filter(Skill.title==skill_title))
    skills = skill.scalars().first()

    if not skills:
        raise ValueError("Нот фоунд")

    questions = await session.execute(select(Question).filter(Question.skill_id==skills.id))
    result = questions.scalars().all()

    return result

async def get_skill_pagination(session, page: int, limit: int = 5):
    offset = (page - 1) * limit

    result = await session.execute(select(Skill.title).order_by(Skill.id).limit(limit).offset(offset))
    skills = result.scalars().all()

    return skills

async def get_total_items(session):
    query = select(func.count()).select_from(Skill)
    result = await session.execute(query)
    return result.scalar()