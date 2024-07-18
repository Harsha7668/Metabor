import motor.motor_asyncio
from config import DATABASE_NAME, DATABASE_URI

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users_col = self.db.users  # Collection for storing user settings
        self.files_col = self.db.files  # Collection for storing file-related settings (thumbnails, etc.)
    
    async def update_user_settings(self, user_id, settings):
        await self.users_col.update_one({'id': user_id}, {'$set': {'settings': settings}}, upsert=True)
        
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
    
   
    
    async def save_sample_video_settings(self, user_id, sample_video_duration, screenshots):
        await self.users_col.update_one(
            {'id': user_id}, 
            {'$set': {
                'settings.sample_video_duration': sample_video_duration,
                'settings.screenshots': screenshots
            }},
            upsert=True
        )

    async def get_sample_video_settings(self, user_id):
        user = await self.users_col.find_one({'id': user_id})
        if user:
            settings = user.get('settings', {})
            sample_video_duration = settings.get('sample_video_duration', "Not set")
            screenshots = settings.get('screenshots', "Not set")
            return sample_video_duration, screenshots
        return "Not set", "Not set"
        
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
            return user.get('settings', {}).get('metadata_titles', {})
        return {}
    
    async def save_screenshots_count(self, user_id, screenshots_count):
        await self.users_col.update_one(
            {'id': user_id},
            {'$set': {'settings.screenshots_count': screenshots_count}},
            upsert=True
        )
    
    async def get_screenshots_count(self, user_id):
        user = await self.users_col.find_one({'id': user_id})
        if user:
            return user.get('settings', {}).get('screenshots_count')
        return None
    
    async def get_sample_video_duration(self, user_id):
        user = await self.users_col.find_one({'id': user_id})
        if user:
            return user.get('settings', {}).get('sample_video_duration')
        return None
    
   
    async def save_thumbnail(self, user_id, file_id):
        await self.files_col.update_one({'id': user_id}, {'$set': {'thumbnail_file_id': file_id}}, upsert=True)
        
    async def get_thumbnail(self, user_id):
        file_data = await self.files_col.find_one({'id': user_id})
        if file_data:
            return file_data.get('thumbnail_file_id')
        return None


    
    async def delete_thumbnail(self, user_id):
        await self.files_col.update_one({'id': user_id}, {'$unset': {'thumbnail_file_id': ""}})
    
    async def save_attach_photo(self, user_id, file_id):
        await self.files_col.update_one({'id': user_id}, {'$set': {'attach_photo_file_id': file_id}}, upsert=True)
    
    async def get_attach_photo(self, user_id):
        file_data = await self.files_col.find_one({'id': user_id})
        if file_data:
            return file_data.get('attach_photo_file_id')
        return None

    async def save_merge_state(self, user_id, merge_state):
        try:
            await self.merge_col.update_one(
                {'id': user_id},
                {'$set': {'merge_state': merge_state}},
                upsert=True
            )
        except Exception as e:
            print(f"Error saving merge state to database: {e}")
            # Handle the error accordingly (logging, exception handling, etc.)

    async def get_merge_state(self, user_id):
        merge_state = await self.merge_col.find_one({'id': user_id})
        if merge_state:
            return merge_state.get('merge_state', {})
        return {}

    async def clear_merge_state(self, user_id):
        try:
            await self.merge_col.delete_one({'id': user_id})
        except Exception as e:
            print(f"Error clearing merge state from database: {e}")
            # Handle the error accordingly (logging, exception handling, etc.)

    async def save_merged_file_info(self, user_id, output_filename, file_size):
        try:
            await self.users_col.update_one(
                {'id': user_id},
                {'$set': {
                    'merged_file_info': {
                        'output_filename': output_filename,
                        'file_size': file_size
                    }
                }},
                upsert=True
            )
        except Exception as e:
            print(f"Error saving merged file info to database: {e}")
            # Handle the error accordingly (logging, exception handling, etc.)

    async def get_merged_file_info(self, user_id):
        user = await self.users_col.find_one({'id': user_id})
        if user:
            return user.get('merged_file_info', {})
        return {}

    async def clear_merged_file_info(self, user_id):
        try:
            await self.users_col.update_one(
                {'id': user_id},
                {'$unset': {'merged_file_info': ""}}
            )
        except Exception as e:
            print(f"Error clearing merged file info from database: {e}")
            # Handle the error accordingly (logging, exception handling, etc.)

    async def save_new_filename(user_id, new_filename):
    # Save new filename information to MongoDB
    await files_col.update_one(
        {'id': user_id},
        {'$set': {'new_filename': new_filename}},
        upsert=True
    )

    async def get_new_filename(user_id):
    # Retrieve new filename information from MongoDB
    file_data = await files_col.find_one({'id': user_id})
    if file_data:
        return file_data.get('new_filename')
    return None


    async def save_screenshot_paths(self, user_id, screenshot_paths):
        result = await self.users_col.update_one(
            {'_id': user_id},
            {'$set': {'screenshot_paths': screenshot_paths}},
            upsert=True
        )
        return result

    async def get_screenshot_paths(self, user_id):
        user = await self.users_col.find_one({'_id': user_id})
        if user:
            return user.get('screenshot_paths', [])
        return []

    async def delete_screenshot_paths(self, user_id):
        result = await self.users_col.update_one(
            {'_id': user_id},
            {'$unset': {'screenshot_paths': ''}}
        )
        return result.modified_count > 0

   
    async def save_extracted_files(self, user_id, file_list):
        await self.files_col.update_one(
            {'id': user_id},
            {'$set': {'extracted_files': file_list}},
            upsert=True
        )

    async def get_extracted_files(self, user_id):
        file_data = await self.files_col.find_one({'id': user_id})
        if file_data:
            return file_data.get('extracted_files', [])
        return []

    
    async def save_user_quality_selection(user_id, selection_data):
    await users_col.update_one({'id': user_id}, {'$set': {'settings.quality_selection': selection_data}}, upsert=True)
    
    async def get_user_quality_selection(user_id):
    user = await users_col.find_one({'id': user_id})
    if user:
        return user.get('settings', {}).get('quality_selection')
    return None
    
    async def close(self):
        self._client.close()


# Initialize the database instance
db = Database(DATABASE_URI, DATABASE_NAME)
