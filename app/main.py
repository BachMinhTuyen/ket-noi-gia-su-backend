from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from app.api.v1 import router as api_v1_router
from app.core.database import database, setup_database
from app.initial_data import create_initial_roles, create_initial_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    try:
        # async with database.get_session() as db:
        db_gen = database.get_session()
        db = await anext(db_gen)
        await create_initial_roles(db)
        await create_initial_admin(db)
        logging.info("Initial roles and admin user created.")
    except Exception as e:
        logging.error("Error creating initial data.")
        logging.error(str(e))

    yield
    await database.close_database()

app = FastAPI(
    lifespan=lifespan,
    title="Connect With Tutor",
    description="A platform to connect with tutors",
    version="1.0.0",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World"}