import math, time
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import heroku3
import os
from Database.database import db
from pyrogram import Client, filters


PROGRESS_BAR_TEMPLATE = """
╭───[**•PROGRESS BAR•**]───⍟
│
├<b>{5}</b>
│
├<b>📁**PROCESS** : {1} | {2}</b>
│
├<b>🚀**PERCENT** : {0}%</b>
│
├<b>⚡**SPEED** : {3}</b>
│
├<b>⏱️**ETA** : {4}</b>
│
╰─────────────────⍟"""

async def start_task(chat_id, message_id, task_id):
    start_time = time.time()
    await db.create_task(task_id, chat_id, message_id)
    # You may need to initialize the task with some initial progress
    await update_task_progress(task_id, 0, 100)  # Example progress

# Example usage:
task_list = [
    ('task1', (50, 100)),
    ('task2', (75, 100)),
]

await progress_message(task_list)
async def update_task_progress(task_id, current, total):
    task = await db.get_task(task_id)
    if not task:
        return

    now = time.time()
    diff = now - task['start_time'].timestamp()
    percentage = current * 100 / total if total else 0
    speed = humanbytes(current / diff) + "/s"
    elapsed_time_ms = round(diff * 1000)
    time_to_completion_ms = round((total - current) / (current / diff)) * 1000 if current else 0
    estimated_total_time_ms = elapsed_time_ms + time_to_completion_ms

    elapsed_time = TimeFormatter(elapsed_time_ms)
    estimated_total_time = TimeFormatter(estimated_total_time_ms)

    progress = "{0}{1}".format(
        ''.join(["■" for _ in range(math.floor(percentage / 5))]),
        ''.join(["□" for _ in range(20 - math.floor(percentage / 5))])
    )

    text = f"{PROGRESS_BAR_TEMPLATE.format(round(percentage, 2), humanbytes(current), humanbytes(total), speed, estimated_total_time if estimated_total_time != '' else '0 s', progress)}\n\n/Cancel_{task_id}"

    try:
        await app.edit_message_text(
            chat_id=task['chat_id'],
            message_id=task['message_id'],
            text=text,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Refresh Status", callback_data=f"refresh_{task_id}")]])
        )
        await db.update_task(task_id, current, total)  # Update the task in the database
    except Exception as e:
        print(f"Error editing message: {e}")

async def progress_message(task_list):
    for task_id, (current, total) in task_list:
        await update_task_progress(task_id, current, total)

@Client.on_callback_query()
async def handle_callback(client, callback_query):
    data = callback_query.data
    if data.startswith("refresh_"):
        task_id = data.split("_")[1]
        task = await db.get_task(task_id)
        if task:
            await update_task_progress(task_id, task['current'], task['total'])
        await callback_query.answer()  # Acknowledge the callback

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



#ALL FILES UPLOADED - CREDITS 🌟 - @Sunrises_24
def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)

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
            
