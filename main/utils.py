import math, time
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import heroku3
import os
from Database.database import db
from pyrogram import Client, filters



PROGRESS_BAR = """
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

def generate_progress_message(current, total, ud_type, start):
    now = time.time()
    diff = now - start
    percentage = current * 100 / total
    speed = humanbytes(current / diff) + "/s"
    elapsed_time_ms = round(diff * 1000)
    time_to_completion_ms = round((total - current) / (current / diff)) * 1000
    estimated_total_time_ms = elapsed_time_ms + time_to_completion_ms

    elapsed_time = TimeFormatter(elapsed_time_ms)
    estimated_total_time = TimeFormatter(estimated_total_time_ms)

    progress = "{0}{1}".format(
        ''.join(["■" for i in range(math.floor(percentage / 5))]),
        ''.join(["□" for i in range(20 - math.floor(percentage / 5))])
    )

    return PROGRESS_BAR.format(
        round(percentage, 2),
        humanbytes(current),
        humanbytes(total),
        speed,
        estimated_total_time if estimated_total_time != '' else '0 s',
        progress
    )

async def progress_message(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
        progress_text = generate_progress_message(current, total, ud_type, start)
        try:
            await message.edit(
                text=f"{ud_type}\n\n" + progress_text,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌟 Jᴏɪɴ Us 🌟", url="https://t.me/Sunrises24botupdates")]])
            )
        except Exception as e:
            print(f"Error editing message: {e}")



class ProgressManager:
    def __init__(self):
        self.tasks = {}

    def start_task(self, task_id, total, ud_type):
        self.tasks[task_id] = {
            'current': 0,
            'total': total,
            'ud_type': ud_type,
            'start': time.time()
        }

    def update_task(self, task_id, current):
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task['current'] = current
            return progress_message(
                task['current'], task['total'], task['ud_type'], task['start']
            )
        return None

    def cancel_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]
            return f"Task {task_id} cancelled."
        return "Task not found."

    def list_progress(self):
        return {
            task_id: progress_message(
                task['current'], task['total'], task['ud_type'], task['start']
            )
            for task_id, task in self.tasks.items()
        }

# Example usage
progress_manager = ProgressManager()
progress_manager.start_task('task1', 83.33 * 1024 * 1024, 'Task 1')
progress_manager.start_task('task2', 100 * 1024 * 1024, 'Task 2')

# Simulate updating tasks
time.sleep(1)
print(progress_manager.update_task('task1', 14.0 * 1024 * 1024))
print(progress_manager.update_task('task2', 50.0 * 1024 * 1024))

# List all progress
print(progress_manager.list_progress())

# Cancel a task
print(progress_manager.cancel_task('task1'))

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
            
