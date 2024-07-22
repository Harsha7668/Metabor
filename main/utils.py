import math, time
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import heroku3
import os
from Database.database import db
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

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
├<b>❌**CANCEL** : {6}</b>
╰─────────────────⍟"""

async def progress_message(current, total, ud_type, message, start, process_id):
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
        cancel_command = f"/cancel_{process_id}"
        tmp = progress + f"\nProgress: {round(percentage, 2)}%\n{humanbytes(current)} of {humanbytes(total)}\nSpeed: {speed}\nETA: {estimated_total_time if estimated_total_time != '' else '0 s'}"

        try:
            process = await db.get_process(process_id)
            if process and process['status'] == 'cancelled':
                await message.edit(text="Process cancelled by user.")
                return True

            await message.edit(
                text=f"{ud_type}\n\n" + PROGRESS_BAR.format(
                    round(percentage, 2),
                    humanbytes(current),
                    humanbytes(total),
                    speed,
                    estimated_total_time if estimated_total_time != '' else '0 s',
                    progress,
                    cancel_command
                ),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌟 Jᴏɪɴ Us 🌟", url="https://t.me/Sunrises24botupdates")]])
            )
        except Exception as e:
            print(f"Error editing message: {e}")





@Client.on_callback_query(filters.regex(r'^cancel_(\w+)$'))
async def handle_cancel_callback(bot, callback_query: CallbackQuery):
    process_id = callback_query.data.split("_")[1]

    # Find and cancel the process
    process = await db.get_process(process_id)
    if not process:
        await callback_query.answer("No such process found.")
        return

    # Update the process status to cancelled
    await db.cancel_process(process_id)

    await callback_query.answer(f"Process {process_id} has been cancelled.")
    await callback_query.message.edit_text(f"Process {process_id} has been cancelled.")

# Function to format time in human-readable format
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

# Function to convert bytes to human-readable format
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

