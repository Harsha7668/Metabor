#ALL FILES UPLOADED - CREDITS 🌟 - @Sunrises_24
import re
from os import environ
import os

id_pattern = re.compile(r'^.\d+$')


API_ID = int(os.environ.get("API_ID", "10811400"))
API_HASH = os.environ.get("API_HASH", "191bf5ae7a6c39771e7b13cf4ffd1279")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7090403697:AAGjSKZOl_kPksvKJNaKbiBl5XDI0tt5QpY")
ADMIN = int(os.environ.get("ADMIN", '6469754522')) 
FSUB_UPDATES = os.environ.get("FSUB_CHANNEL", "Sunrises24BotUpdates")
FSUB_GROUP = os.environ.get("FSUB_GROUP", "Sunrises24BotSupport")
CAPTION = os.environ.get("CAPTION", "")
#ALL FILES UPLOADED - CREDITS 🌟 - @Sunrises_24
DOWNLOAD_LOCATION = "./DOWNLOADS"
SUNRISES_PIC= "https://graph.org/file/bd91761f6e938e2e6d23a.jpg"  # Replace with your Telegraph link
AUTH_USERS = int(os.environ.get("AUTH_USERS", '6469754522'))

DATABASE_NAME = os.environ.get("DATABASE_NAME", "cluster0")

DATABASE_URI = os.environ.get("DATABASE_URI", "mongodb+srv://INFINITYRENAME24BOT:INFINITYRENAME24BOT@cluster0.colorb9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


