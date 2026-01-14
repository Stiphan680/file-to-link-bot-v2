from motor.motor_asyncio import AsyncIOMotorClient
from info import DATABASE_URI, DATABASE_NAME
from bson import ObjectId
import json

class BatchDatabase:
    def __init__(self):
        self._client = AsyncIOMotorClient(DATABASE_URI)
        self.db = self._client[DATABASE_NAME]
        self.batches = self.db.batches

    async def create_batch(self, user_id, batch_data):
        result = await self.batches.insert_one({
            'user_id': user_id,
            'batch_data': batch_data
        })
        return str(result.inserted_id)

    async def get_batch(self, batch_id):
        try:
            batch = await self.batches.find_one({'_id': ObjectId(batch_id)})
            return batch
        except:
            return None

batch_db = BatchDatabase()
