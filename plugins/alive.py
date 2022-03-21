import asyncio
from time import time
from datetime import datetime
from modules.helpers.filters import command
from modules.helpers.command import commandpro
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)
    
   

@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/3f87af079e460935fb8fa.jpg",
        caption=f"""**I ᴀᴍ 𝙉𝙖𝙫𝙔𝙖 𝙈𝙐𝙎𝙄𝘾 𝘽𝙊𝙏
ʙᴏᴛ ʜᴀɴᴅʟᴇ ʙʏ [𝙉𝙖𝙫𝙮𝙖](https://t.me/WTF_NAVYA)**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        " ❰𝐆𝐫𝐨𝐮𝐩 𝐒𝐮𝐩𝐩𝐨𝐫𝐭❱ ", url=f"https://t.me/NavyaSupport")
                ]
                
           ]
        ),
    )
    
    
@Client.on_message(commandpro(["/start", "hi", "Navya"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/06f33456a78b0161843d8.jpg",
        caption=f"""Hi☺️""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        " ❰𝐆𝐫𝐨𝐮𝐩 𝐒𝐮𝐩𝐩𝐨𝐫𝐭❱ ", url=f"https://t.me/TheNavya")
                ]
            ]
        ),
    )


@Client.on_message(commandpro(["repo", "#repo", "@repo", "/repo", "source"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/f01b866242fa4e3bf74ad.jpg",
        caption=f"""""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        " ❰𝙍𝙚𝙥𝙤𝙨𝙞𝙩𝙤𝙧𝙮❱ ", url=f"https://t.me/TheNavya")
                ]
            ]
        ),
    )
