import math, time
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import heroku3
import os
from Database.database import db
from pyrogram import Client, filters


# Define the progress bar template
PROGRESS_BAR_TEMPLATE = """
╭───[•PROGRESS BAR•]───⍟
│
├{progress}
│
├📁PROCESS : {current} | {total}
│
├🚀PERCENT : {percentage}%
│
├⚡SPEED : {speed}
│
├⏱️ETA : {eta}
│
╰─────────────────⍟
"""

# Convert bytes to human-readable format
def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

# Format elapsed and remaining time
def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
          ((str(hours) + "h, ") if hours else "") + \
          ((str(minutes) + "m, ") if minutes else "") + \
          ((str(seconds) + "s, ") if seconds else "") + \
          ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

# Generate the progress message
def generate_progress_message(current, total, speed, eta):
    percentage = round(current * 100 / total, 2)
    progress_bar = ''.join(["■" for _ in range(int(percentage / 5))]) + ''.join(["□" for _ in range(20 - int(percentage / 5))])
    formatted_current = humanbytes(current)
    formatted_total = humanbytes(total)
    
    return PROGRESS_BAR_TEMPLATE.format(
        progress=progress_bar,
        current=formatted_current,
        total=formatted_total,
        percentage=percentage,
        speed=speed,
        eta=eta
    )

# Example usage of the progress bar
current = 14.0 * 2**20  # 14 MB in bytes
total = 83.33 * 2**20   # 83.33 MB in bytes
speed = "1.36 MB/s"
eta = "1m, 1s, 268ms"

progress_message = generate_progress_message(current, total, speed, eta)
print("🚀 Download Started... ⚡️\n")
print(progress_message)
print("\n/Cancel_user_id")



#ALL FILES UPLOADED - CREDITS 🌟 - @Sunrises_24
# Define heroku_restart function
async def heroku_restart():
    HEROKU_API = "HRKU-987b360b-e27e-43bf-b4e8-026e4c07521e"
    HEROKU_APP_NAME = "infinitystartrename24bot"
    x = None
    if not HEROKU_API or not HEROKU_APP_NAME:
        x = None
    else:
        try:
            acc = heroku3.from_key(HEROKU_API)
            bot = acc.apps()[HEROKU_APP_NAME]
            bot.restart()
            x = True
        except Exception as e:
            print(e)
            x = False
    return x

#ALL FILES UPLOADED - CREDITS 🌟 - @Sunrises_24
#for merging downloading media
async def download_media(msg, sts):
    c_time = time.time()
    try:
        file_path = await msg.download(progress=progress_message, progress_args=("🚀 Downloading media... ⚡", sts, c_time))
        await msg.reply_text(f"✅ Media downloaded successfully: {os.path.basename(file_path)}")
        return file_path
    except Exception as e:
        await sts.edit(f"❌ Error downloading media: {e}")
        raise

#ALL FILES UPLOADED - CREDITS 🌟 - @Sunrises_24        
# Recursive function to upload files
async def upload_files(bot, chat_id, directory, base_path=""):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            try:
                await bot.send_document(chat_id, document=item_path, caption=item)
            except Exception as e:
                print(f"Error uploading {item}: {e}")
        elif os.path.isdir(item_path):
            await upload_files(bot, chat_id, item_path, base_path=os.path.join(base_path, item))
            
