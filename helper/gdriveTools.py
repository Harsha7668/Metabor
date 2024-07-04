import os
import pathlib
import pickle
import time
import urllib.parse as urlparse
from urllib.parse import parse_qs

import re
import json

import requests

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from tenacity import *

from helper_funcs.bot_utils import setInterval

# Constants and global variables
SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
download_dict = {}

class GoogleDriveHelper:
    def __init__(self, name=None):
        self.__G_DRIVE_TOKEN_FILE = "token.pickle"
        self.__OAUTH_SCOPE = ['https://www.googleapis.com/auth/drive']
        self.__REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
        self.__G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"
        self.__G_DRIVE_BASE_DOWNLOAD_URL = "https://drive.google.com/uc?id={}&export=download"
        self.__G_DRIVE_DIR_BASE_DOWNLOAD_URL = "https://drive.google.com/drive/folders/{}"
        self.__service = self.authorize()
        self.name = name

    def getIdFromUrl(self, link):
        if "folders" in link or "file" in link:
            regex = r"https://drive\.google\.com/(drive)?/?\d?/?(mobile)?/?(file)?(folders)?/?d?/([-\w]+)[?+]?/?(w+)?"
            res = re.search(regex, link)
            if res is None:
                raise IndexError("GDrive ID not found.")
            return res.group(5)
        parsed = urlparse.urlparse(link)
        return parse_qs(parsed.query)['id'][0]

    @retry(wait=wait_exponential(multiplier=2, min=3, max=6), stop=stop_after_attempt(5),
           retry=retry_if_exception_type(HttpError))
    def upload_file(self, file_path, file_name, mime_type, parent_id):
        file_metadata = {
            'name': file_name,
            'description': 'mirror',
            'mimeType': mime_type,
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]

        media_body = MediaFileUpload(file_path,
                                     mimetype=mime_type,
                                     resumable=True,
                                     chunksize=50 * 1024 * 1024)

        drive_file = self.__service.files().create(supportsTeamDrives=True,
                                                   body=file_metadata, media_body=media_body)

        response = None
        while response is None:
            try:
                self.status, response = drive_file.next_chunk()
            except HttpError as err:
                if err.resp.get('content-type', '').startswith('application/json'):
                    reason = json.loads(err.content).get('error').get('errors')[0].get('reason')
                    if reason in ['userRateLimitExceeded', 'dailyLimitExceeded']:
                        LOGGER.info(f"Got: {reason}, Retrying...")
                        continue
                raise err

        drive_file = self.__service.files().get(supportsTeamDrives=True, fileId=response['id']).execute()
        download_url = self.__G_DRIVE_BASE_DOWNLOAD_URL.format(drive_file.get('id'))
        return download_url

    def authorize(self):
        credentials = None
        if os.path.exists(self.__G_DRIVE_TOKEN_FILE):
            with open(self.__G_DRIVE_TOKEN_FILE, 'rb') as f:
                credentials = pickle.load(f)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.__OAUTH_SCOPE)
                credentials = flow.run_console(port=0)

            with open(self.__G_DRIVE_TOKEN_FILE, 'wb') as token:
                pickle.dump(credentials, token)

        return build('drive', 'v3', credentials=credentials, cache_discovery=False)

    def escapes(self, string):
        chars = ['\\', "'", '"', r'\a', r'\b', r'\f', r'\n', r'\r', r'\t']
        for char in chars:
            string = string.replace(char, '\\' + char)
        return string
