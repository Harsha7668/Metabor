import math, time
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import heroku3
import os
from config import *
from pyrogram import Client, filters




# Dictionary to keep track of ongoing processes
processes = {}

# Dictionary to map user IDs to usernames
usernames = {}

async def progress_message(current, total, ud_type, message, start, initiator_id, initiator_username):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
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
        tmp = progress + f"\nProgress: {round(percentage, 2)}%\n{humanbytes(current)} of {humanbytes(total)}\nSpeed: {speed}\nETA: {estimated_total_time if estimated_total_time != '' else '0 s'}"

        # Store process details
        processes[message.message_id] = {
            'initiator_id': initiator_id,
            'initiator_username': initiator_username,
            'status': 'Downloading',
            'task': asyncio.create_task(handle_process(current, total, message))
        }

        try:
            await message.edit(
                text=f"{ud_type}\n\n" + PROGRESS_BAR.format(
                    round(percentage, 2),
                    humanbytes(current),
                    humanbytes(total),
                    speed,
                    estimated_total_time if estimated_total_time != '' else '0 s',
                    progress
                ),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cʟᴏꜱᴇ ❌", callback_data=f"del_{message.message_id}")]])
            )
        except Exception as e:
            print(f"Error editing message: {e}")

async def handle_process(current, total, message):
    # Example task to simulate a process
    while current < total:
        await asyncio.sleep(1)
        # Update process status here
        current += 1
        # Handle process updates here
        # Check for cancellation
        if message.message_id not in processes:
            break

@Client.on_callback_query(filters.regex(r"del_(\d+)"))
async def cancel_process(bot, msg):
    message_id = int(msg.matches[0].group(1))
    user_id = msg.from_user.id

    if user_id not in ADMIN and processes.get(message_id, {}).get('initiator_id') != user_id:
        # Ignore cancellation request if the user is not the initiator or an admin
        return

    if message_id in processes:
        task = processes[message_id]['task']
        if not task.done():
            task.cancel()  # Cancel the task
            processes.pop(message_id, None)  # Remove process from tracking

        try:
            await msg.message.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")




#ALL FILES UPLOADED - CREDITS 🌟 - @Sunrises_24
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

#ALL FILES UPLOADED - CREDITS 🌟 - @Sunrises_24
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
            
