import motor.motor_asyncio
from pyrogram import Client, filters
from info import DATABASE_NAME, DATABASE_URI
  
# Initialize MongoDB client
mongo_client = motor.motor_asyncio.AsyncIOMotorClient('uri')
db = mongo_client['your_database_name']
user_settings_collection = db['user_settings']

class UserSettingsDB:
    def __init__(self, collection):
        self.collection = collection

    async def update_settings(self, user_id, settings):
        await self.collection.update_one({'user_id': int(user_id)}, {'$set': {'settings': settings}}, upsert=True)

    async def get_settings(self, user_id):
        default = {
            'sample_video_duration': 'Not set',
            'screenshots': 'Not set',
            'thumbnail': 'Not set',
            'metadata': {
                'video_title': 'Not set',
                'audio_title': 'Not set',
                'subtitle_title': 'Not set'
            },
            'attach_photo': 'Not set',
            'photo': 'Not set',
            'gofile_api_key': 'Not set',
            'gdrive_folder_id': 'Not set'
        }
        user = await self.collection.find_one({'user_id': int(user_id)})
        if user:
            return user.get('settings', default)
        return default

db = Database(DATABASE_URI, DATABASE_NAME)
