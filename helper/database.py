from motor.motor_asyncio import AsyncIOMotorClient
from bson.errors import InvalidId
from bson import ObjectId
from .utils import get_date
from config import Config
from datetime import datetime


class Database:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.groups = self.db.groups
    
    async def add_user(self, group_id, user, days):
        if not await self.is_user_exist(user.id, group_id):
            validity, expired_on = get_date(days)
            data = dict(
                id=user.id,
                group_id=group_id,
                validity=validity,
                expired_on=expired_on,
                link_used=False
            )
            await self.col.insert_one(data)
            return await self.get_user(user.id, group_id)
        return await self.get_user(user.id, group_id)
    
    async def check_user(self, id, key):
        try:
            user = await self.col.find_one({'_id': ObjectId(key)})           
        except InvalidId:
            return Config.INVALID_KEY

        if not user:
            return Config.USER_NOT_EXIST 

        if int(user['id']) != id:
            return Config.USER_NOT_MATCH 

        if bool(user['link_used']) == True:       
            return Config.LINK_USED
            
        await self.link_used(id, True)
        return Config.LINK_SUCCESS 

    async def link_used(self, id, status=True):
        await self.col.update_one({'id': id}, {'$set': {'link_used': status}})

    async def is_user_exist(self, id, group_id):
        user = await self.col.find_one({'id': int(id), 'group_id': group_id})
        return bool(user)
    
    async def get_user(self, id, group_id):
        return await self.col.find_one({'id': int(id), 'group_id': group_id}) or None
       
    async def get_users_by_id(self, id):
        cursor = self.col.find({'id': int(id)})
        return await cursor.to_list(length=None)
     

    # ✅ FIXED FUNCTION
    async def total_users_count(self):
        return await self.col.count_documents({})


    async def get_all_users(self):
        return self.col.find({})
    

    async def delete_user(self, id):
        await self.col.delete_many({'id': int(id)})


    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']


    # -------------------- GROUP MANAGEMENT --------------------

    async def add_group(self, group_id, title, price):
        data = dict(
            group_id=int(group_id),
            title=title,
            price=int(price),
            created_at=datetime.now()
        )

        if await self.groups.find_one({'group_id': group_id}):
            return False

        await self.groups.insert_one(data)
        return True


    async def list_groups(self):
        cursor = self.groups.find({})
        return await cursor.to_list(length=None)
        

    async def get_group(self, key):
        return await self.groups.find_one({'_id': ObjectId(key)}) or None       


    async def update_group_id(self, key, group_id, title, price):
        await self.groups.update_one(
            {'_id': ObjectId(key)},
            {'$set': {'group_id': group_id}}
        )


    async def update_group_title(self, key, title):
        await self.groups.update_one(
            {'_id': ObjectId(key)},
            {'$set': {'title': title}}
        )


    async def update_group_price(self, key, price):
        await self.groups.update_one(
            {'_id': ObjectId(key)},
            {'$set': {'price': price}}
        )
    

    # ✅ FIXED HERE
    async def delete_group(self, key):
        await self.groups.delete_one({'_id': ObjectId(key)})
        await self.col.delete_many({'group_id': ObjectId(key)})


    async def get_users_by_group(self, key):
        cursor = self.col.find({'group_id': ObjectId(key)})
        return await cursor.to_list(length=None)


db = Database(Config.DB_URL, Config.DB_NAME)
