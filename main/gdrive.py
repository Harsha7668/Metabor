import os
import time
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from main.utils import progress_message
import re
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Function to authenticate Google Drive
def authenticate_google_drive():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

# Authenticate and create the Drive service
creds = authenticate_google_drive()
drive_service = build('drive', 'v3', credentials=creds)

async def upload_to_google_drive(file_path, file_name, sts):
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, resumable=True)
    request = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink')

    response = None
    start_time = time.time()
    while response is None:
        status, response = request.next_chunk()
        if status:
            await progress_message(status.resumable_progress, os.path.getsize(file_path), "Uploading to Google Drive", sts, start_time)

    return response.get('webViewLink')

# Extract the file ID from a Google Drive URL
def extract_id_from_url(url):
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
    return match.group(1) if match else None



# Copy a file to a new folder in Google Drive
def copy_file(file_id, new_folder_id):
    try:
        file = drive_service.files().get(fileId=file_id, fields='name').execute()
        copied_file = {'name': file['name'], 'parents': [new_folder_id]}
        return drive_service.files().copy(fileId=file_id, body=copied_file).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


