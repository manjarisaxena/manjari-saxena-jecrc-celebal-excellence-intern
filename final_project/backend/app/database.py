from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


class Database:
    client: AsyncIOMotorClient = None
    db = None


db_helper = Database()


async def connect_to_mongo():
    db_helper.client = AsyncIOMotorClient(settings.MONGO_URI)
    db_helper.db = db_helper.client.get_default_database()
    # Helpful indexes
    await db_helper.db.users.create_index("email", unique=True)


async def close_mongo_connection():
    if db_helper.client:
        db_helper.client.close()
