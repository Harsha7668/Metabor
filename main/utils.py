import math, time
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import heroku3
import os, asyncio


#ALL FILES UPLOADED - CREDITS 🌟 - @Sunrises_24
PROGRESS_BAR = """
╭───[**•PROGRESS BAR•**]───⍟
├<b>{5}</b>
├<b>📁**PROCESS** : {1} | {2}</b>
├<b>🚀**PERCENT** : {0}%</b>
├<b>⚡**SPEED** : {3}</b>
├<b>⏱️**ETA** : {4}</b>
╰─────────────────⍟"""

#ALL FILES UPLOADED - CREDITS 🌟 - @Sunrises_24
async def progress_message(current, total, ud_type, message, start):
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
            ''.join(["▣" for i in range(math.floor(percentage / 5))]),
            ''.join(["▢" for i in range(20 - math.floor(percentage / 5))])
        )
        tmp = progress + f"\nProgress: {round(percentage, 2)}%\n{humanbytes(current)} of {humanbytes(total)}\nSpeed: {speed}\nETA: {estimated_total_time if estimated_total_time != '' else '0 s'}"

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
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌟 Jᴏɪɴ Us 🌟", url="https://t.me/Sunrises24botupdates")]])
            )
        except Exception as e:
            print(f"Error editing message: {e}")
            


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
# Recursive function to upload file
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
        
async def convert_video(video_file, output_file, bot, msg, sts):
    progress = "progress.txt"
    command = (
        f"ffmpeg -hide_banner -loglevel quiet -progress {progress} -i {video_file} "
        f"-vf drawtext=fontfile=font.ttf:fontsize=27:fontcolor=white:bordercolor=black@0.50:x=w-tw-10:y=10:box=1:boxcolor=black@0.5:boxborderw=6:text='@Anime_Sensei' "
        f"-c:v libx264 -crf 28 -pix_fmt yuv420p -s 854x480 -b:v 150k -c:a libopus -b:a 35k -preset veryfast {output_file} -y"
    )

    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    COMPRESSION_START_TIME = time.time()
    while process.returncode is None:
        await asyncio.sleep(3)
        with open(progress, 'r') as file:
            text = file.read()
            frame = re.findall("frame=(\d+)", text)
            time_in_us = re.findall("out_time_ms=(\d+)", text)
            progress = re.findall("progress=(\w+)", text)
            speed = re.findall("speed=(\d+\.?\d*)", text)
            if frame:
                frame = int(frame[-1])
            else:
                frame = 1
            if speed:
                speed = speed[-1]
            else:
                speed = 1
            if time_in_us:
                time_in_us = time_in_us[-1]
            else:
                time_in_us = 1
            if progress and progress[-1] == "end":
                break

            elapsed_time = int(time_in_us) / 1000000
            execution_time = int((time.time() - COMPRESSION_START_TIME) * 1000)
            difference = math.floor((elapsed_time / float(speed)))
            ETA = "-" if difference <= 0 else TimeFormatter(difference * 1000)
            percentage = math.floor(elapsed_time * 100 / execution_time)
            progress_str = f"📈 <b>Progress:</b> {round(percentage, 2)}%\n" \
                           f"[{'█' * math.floor(percentage / 10)}{'.' * (10 - math.floor(percentage / 10))}]"
            stats = f'🗳 <b>ENCODING IN PROGRESS</b>\n\n' \
                    f'⌚ <b>TIME LEFT:</b> {ETA}\n\n' \
                    f'{progress_str}\n'

            try:
                await msg.edit_text(stats)
            except:
                pass

    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    if process.returncode != 0:
        await msg.edit_text(f"**ERROR:** {e_response}\n\nContact @TheBatmanShan")
        os.remove(video_file)
        os.remove(output_file)
        return None

    if os.path.exists(output_file):
        return output_file
    else:
        return None
