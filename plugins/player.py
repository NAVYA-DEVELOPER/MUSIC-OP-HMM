# LGcYALEX // @LGcYALEX

import os
import aiofiles
import aiohttp
import ffmpeg
import requests
from os import path
from asyncio.queues import QueueEmpty
from typing import Callable
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from modules.cache.admins import set
from modules.clientbot import clientbot, queues
from modules.clientbot.clientbot import client as USER
from modules.helpers.admins import get_administrators
from youtube_search import YoutubeSearch
from modules import converter
from modules.downloaders import youtube
from modules.config import DURATION_LIMIT, que, SUDO_USERS
from modules.cache.admins import admins as a
from modules.helpers.filters import command, other_filters
from modules.helpers.command import commandpro
from modules.helpers.decorators import errors, authorized_users_only
from modules.helpers.errors import DurationLimitError
from modules.helpers.gets import get_url, get_file_name
from PIL import Image, ImageFont, ImageDraw
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

# plus
chat_id = None
useer = "NaN"


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("resource/thumbnail.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("resource/font.otf", 32)
    draw.text((190, 550), f"Title: {title[:50]} ...", (255, 255, 255), font=font)
    draw.text((190, 590), f"Duration: {duration}", (255, 255, 255), font=font)
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text(
        (190, 670),
        f"Powered By: LGcY • ALEX (@LGcYALEX)",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    commandpro(["/play", "/yt", "/ytp", "play", "yt", "ytp", "@", "#"])
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    global que
    global useer
    
    lel = await message.reply("**𝑺𝒆𝒂𝒓𝒄𝒉𝒊𝒏𝒈**\n\n0% ▓▓▓▓▓▓▓▓▓▓▓▓ 100% ...**")

    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "LGCY_Player"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                      "**𝑭𝒂𝒔𝒕 𝑴𝒂𝒌𝒆 𝑴𝒆 𝑨𝒅𝒎𝒊𝒏 ...**")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "** 𝑰 𝒂𝒎 𝒓𝒆𝒂𝒅𝒚 𝒕𝒐 𝒑𝒍𝒂𝒚 ...**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"**𝑷𝒍𝒆𝒂𝒔𝒆 𝑴𝒂𝒏𝒖𝒂𝒍𝒍𝒚 𝑨𝒅𝒅 𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕 𝒐𝒓 𝑪𝒐𝒏𝒕𝒂𝒄𝒕 :-  @LGcYALEX** ")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"**𝑷𝒍𝒆𝒂𝒔𝒆 𝑴𝒂𝒏𝒖𝒂𝒍𝒍𝒚 𝑨𝒅𝒅 𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕 𝒐𝒓 𝑪𝒐𝒏𝒕𝒂𝒄𝒕 :-  @LGcYALEX**")
        return
    
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"**𝑷𝒍𝒂𝒚 𝑴𝒖𝒔𝒊𝒄 𝑳𝒆𝒔𝒔\n 𝑻𝒉𝒂𝒏 {DURATION_LIMIT} 𝑴𝒊𝒏𝒖𝒕𝒆𝒔🤗 ...**"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/86680d3800277ce09ac9f.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="𝐆𝐫𝐨𝐮𝐩 𝐒𝐮𝐩𝐩𝐨𝐫𝐭",
                            url=f"https://t.me/LGCY_OFFICIAL")

                ]
            ]
        )

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="𝐆𝐫𝐨𝐮𝐩 𝐒𝐮𝐩𝐩𝐨𝐫𝐭",
                            url=f"https://t.me/LGCY_OFFICIAL")

                ]
            ]
        )

        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/86680d3800277ce09ac9f.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="𝐆𝐫𝐨𝐮𝐩 𝐒𝐮𝐩𝐩𝐨𝐫𝐭",
                            url=f"https://t.me/LGCY_OFFICIAL")
                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**𝑷𝒍𝒂𝒚 𝑴𝒖𝒔𝒊𝒄 𝑳𝒆𝒔𝒔\n 𝑻𝒉𝒂𝒏 {DURATION_LIMIT} 𝑴𝒊𝒏𝒖𝒕𝒆𝒔🤗 ...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "**𝑮𝒊𝒗𝒆 𝑴𝒖𝒔𝒊𝒄 𝑵𝒂𝒎𝒆\n𝑻𝒐 𝑷𝒍𝒂𝒚...**"
            )
        await lel.edit("**𝑷𝒓𝒐𝒄𝒆𝒔𝒔𝒊𝒏𝒈**\n\n0% ▓▓▓▓▓▓▓▓▓▓▓▓ 100%**")
        query = message.text.split(None, 1)[1]
        # print(query)
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "**𝑴𝒖𝒔𝒊𝒄 𝑵𝒐𝒕 𝑭𝒐𝒖𝒏𝒅...**"
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="𝐆𝐫𝐨𝐮𝐩 𝐒𝐮𝐩𝐩𝐨𝐫𝐭",
                            url=f"https://t.me/LGCY_OFFICIAL")

                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**𝑷𝒍𝒂𝒚 𝑴𝒖𝒔𝒊𝒄 𝑳𝒆𝒔𝒔\n 𝑻𝒉𝒂𝒏 {DURATION_LIMIT} 💞 𝑴𝒊𝒏𝒖𝒕𝒆𝒔🤗...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption="**𝙇𝙂𝙘𝙔・𝙈𝙐𝙎𝙄𝘾 \n𝑨𝒕 𝑷𝒐𝒔𝒊𝒕𝒊𝒐𝒏 » `{}` ...**".format(position),
            reply_markup=keyboard,
        )
    else:
        await clientbot.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )

        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="**𝙇𝙂𝙘𝙔・𝙈𝙐𝙎𝙄𝘾  𝑵𝒐𝒘\n𝑷𝒍𝒂𝒚𝒊𝒏𝒈...**".format(),
           )

    os.remove("final.png")
    return await lel.delete()
    
    
@Client.on_message(commandpro(["/pause", "pause"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    await clientbot.pytgcalls.pause_stream(message.chat.id)
    await message.reply_photo(
                             photo="https://telegra.ph/file/86680d3800277ce09ac9f.jpg", 
                             caption="**𝙇𝙂𝙘𝙔・𝙈𝙐𝙎𝙄𝘾 𝑵𝒐𝒘 \n▶️ 𝑷𝒂𝒖𝒔𝒆𝒅...**"
    )


@Client.on_message(commandpro(["/resume", "resume"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    await clientbot.pytgcalls.resume_stream(message.chat.id)
    await message.reply_photo(
                             photo="https://telegra.ph/file/86680d3800277ce09ac9f.jpg", 
                             caption="**𝙇𝙂𝙘𝙔・𝙈𝙐𝙎𝙄𝘾 𝑵𝒐𝒘\n⏸ 𝑷𝒍𝒂𝒚𝒊𝒏𝒈...**"
    )



@Client.on_message(commandpro(["/skip", "/next", "skip", "next"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("**𝑵𝒐𝒕𝒉𝒊𝒏𝒈 is 𝑷𝒍𝒂𝒚𝒊𝒏𝒈**")
    else:
        queues.task_done(chat_id)
        
        if queues.is_empty(chat_id):
            await clientbot.pytgcalls.leave_group_call(chat_id)
        else:
            await clientbot.pytgcalls.change_stream(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        clientbot.queues.get(chat_id)["file"],
                    ),
                ),
            )


    await message.reply_photo(
                             photo="https://telegra.ph/file/86680d3800277ce09ac9f.jpg", 
                             caption=f'**𝙇𝙂𝙘𝙔・𝙈𝙐𝙎𝙄𝘾 𝑵𝒐𝒘\n⏩ 𝑺𝒌𝒊𝒑𝒑𝒆𝒅.....**'
   ) 


@Client.on_message(commandpro(["/end", "end", "/stop", "stop", "x"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    try:
        clientbot.queues.clear(message.chat.id)
    except QueueEmpty:
        pass

    await clientbot.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_photo(
                             photo="https://telegra.ph/file/86680d3800277ce09ac9f.jpg", 
                             caption="**𝙇𝙂𝙘𝙔・𝙈𝙐𝙎𝙄𝘾 𝑵𝒐𝒘\n 𝑬𝒏𝒅𝒆𝒅...**"
    )


@Client.on_message(commandpro(["reload", "refresh"]))
@errors
@authorized_users_only
async def admincache(client, message: Message):
    set(
        message.chat.id,
        (
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ),
    )

    await message.reply_photo(
                              photo="https://telegra.ph/file/86680d3800277ce09ac9f.jpg",
                              caption="**𝙇𝙂𝙘𝙔・𝙈𝙐𝙎𝙄𝘾 𝑵𝒐𝒘\n 𝑹𝒆𝒍𝒐𝒂𝒅𝒆𝒅...**"
    )
