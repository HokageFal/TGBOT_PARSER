import asyncio
from alembic.config import Config
from alembic import command
from sqlalchemy.ext.asyncio import create_async_engine


async def run_async_migrations():
    # Укажите путь к вашему alembic.ini
    alembic_cfg = Config("alembic.ini")

    # Создаем асинхронное подключение
    engine = create_async_engine(alembic_cfg.get_main_option("sqlalchemy.url"))

    async with engine.connect() as connection:
        await connection.run_sync(
            lambda conn: command.upgrade(alembic_cfg, "head")
        )


if __name__ == "__main__":
    asyncio.run(run_async_migrations())