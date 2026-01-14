from motor.motor_asyncio import AsyncIOMotorClient
from info import DATABASE_URI, DATABASE_NAME

class Database:
    def __init__(self):
        self._client = AsyncIOMotorClient(DATABASE_URI)
        self.db = self._client[DATABASE_NAME]
        self.users = self.db.users

    async def is_user_exist(self, user_id):
        user = await self.users.find_one({'user_id': user_id})
        return bool(user)

    async def add_user(self, user_id, name):
        await self.users.insert_one({
            'user_id': user_id,
            'name': name
        })

    async def total_users_count(self):
        return await self.users.count_documents({})

db = Database()
