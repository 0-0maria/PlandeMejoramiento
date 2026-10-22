import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from beanie import init_beanie
from models import Incidente

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "incidentes_db")

client = AsyncMongoClient(MONGO_URI)

async def init_db():
    database = client[MONGO_DB_NAME]
    await init_beanie(
        database=database,
        document_models=[Incidente],
    )