import motor.motor_asyncio
from config import DATABASE_NAME, DATABASE_URI


class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users_col = self.db.users  # Collection for storing user settings
        self.files_col = self.db.files  # Collection for storing file-related settings (thumbnails, etc.)
    
    async def update_user_settings(self, user_id, settings):
        await self.users_col.update_one({'id': user_id}, {'$set': {'usersettings': settings}}, upsert=True)
        
    async def get_user_settings(self, user_id):
        default_settings = {
            'sample_video_duration': "Not set",
            'screenshots': "Not set",
            'thumbnail_path': None,
            'gofile_api_key': None,
            'gdrive_folder_id': None,
            'metadata_titles': {
                'video_title': '',
                'audio_title': '',
                'subtitle_title': ''
            }
        }
        user = await self.users_col.find_one({'id': user_id})
        if user:
            return user.get('settings', default_settings)
        return default_settings
    
    async def save_thumbnail(self, user_id, thumbnail_path):
        await self.files_col.update_one({'id': user_id}, {'$set': {'thumbnail_path': thumbnail_path}}, upsert=True)
        
    async def get_thumbnail_path(self, user_id):
        file_data = await self.files_col.find_one({'id': user_id})
        if file_data:
            return file_data.get('thumbnail_path')
        return None
    
    async def save_sample_video_settings(self, user_id, sample_video_duration, screenshots):
        await self.users_col.update_one(
            {'id': user_id}, 
            {'$set': {
                'settings.sample_video_duration': sample_video_duration,
                'settings.screenshots': screenshots
            }},
            upsert=True
        )
        
    async def save_gofile_api_key(self, user_id, api_key):
        await self.users_col.update_one({'id': user_id}, {'$set': {'settings.gofile_api_key': api_key}}, upsert=True)
    
    async def get_gofile_api_key(self, user_id):
        user = await self.users_col.find_one({'id': user_id})
        if user:
            return user.get('settings', {}).get('gofile_api_key')
        return None
    
    async def save_gdrive_folder_id(self, user_id, folder_id):
        await self.users_col.update_one({'id': user_id}, {'$set': {'settings.gdrive_folder_id': folder_id}}, upsert=True)
    
    async def get_gdrive_folder_id(self, user_id):
        user = await self.users_col.find_one({'id': user_id})
        if user:
            return user.get('settings', {}).get('gdrive_folder_id')
        return None
    
    async def save_metadata_titles(self, user_id, video_title, audio_title, subtitle_title):
        await self.users_col.update_one(
            {'id': user_id}, 
            {'$set': {
                'settings.metadata_titles.video_title': video_title,
                'settings.metadata_titles.audio_title': audio_title,
                'settings.metadata_titles.subtitle_title': subtitle_title
            }},
            upsert=True
        )
    
    async def get_metadata_titles(self, user_id):
        user = await self.users_col.find_one({'id': user_id})
        if user:
            return user.get('usersettings', {}).get('metadata_titles', {})
        return {}
    
    async def close(self):
        self._client.close()

db = Database(DATABASE_URI, DATABASE_NAME)
      
