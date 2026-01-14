from motor.motor_asyncio import AsyncIOMotorClient
from info import DATABASE_URI, DATABASE_NAME

class FilesDatabase:
    def __init__(self):
        self._client = AsyncIOMotorClient(DATABASE_URI)
        self.db = self._client[DATABASE_NAME]
        self.files = self.db.files

    async def add_file(self, file_id, user_id, file_name):
        await self.files.insert_one({
            'file_id': file_id,
            'user_id': user_id,
            'file_name': file_name
        })

files_db = FilesDatabase()
