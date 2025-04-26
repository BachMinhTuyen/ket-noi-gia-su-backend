from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from typing import AsyncGenerator

from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL
# engine = create_async_engine(DATABASE_URL, echo=True, future=True)
Base = declarative_base()

class Database:
    def __init__(self):
        self.engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
        # self.Base = declarative_base()

    async def create_database(self, database_name: str):
        superuser_database_url = settings.SUPERUSER_DATABASE_URL
        superuser_engine = create_async_engine(superuser_database_url, echo=True, future=True, isolation_level="AUTOCOMMIT")
        try:
            async with superuser_engine.connect() as conn:
                result = await conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{database_name}'"))
                db_exists = result.scalar()
                if not db_exists:
                    await conn.execute(text(f"CREATE DATABASE \"{database_name}\""))
                    print(f"Database '{database_name}' created successfully")
                else:
                    print(f"Database '{database_name}' already exists")
        except ProgrammingError as e:
            print(f"Error creating database: {e}")
        finally:
            await superuser_engine.dispose()

    async def ping_database(self):
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            print("Successfully connected to the Database!")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)
        print("Database tables created successfully")
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    # @asynccontextmanager
    # async def get_session(self) -> AsyncSession:
    #     async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
    #     session = None
    #     try:
    #         session = async_session()
    #         async with session:
    #             yield session
    #     except Exception as e:
    #         await session.rollback()
    #         raise e
    #     finally:
    #         await session.close()

    async def close_database(self):
        await self.engine.dispose()
        print("Database connection closed!")

database = Database()
async def setup_database():
    # await database.create_database(settings.DATABASE_NAME)
    await database.ping_database()
    # await database.create_tables()