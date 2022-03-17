# Copyright (C) 2021 By AdityaPlayer

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Dialog, Chat, Message
from pyrogram.errors import UserAlreadyParticipant
from modules.clientbot.clientbot import client as aditya
from modules.config import SUDO_USERS

@Client.on_message(filters.command(["gcast", "post", "send"]))
async def broadcast(_, message: Message):
    sent=0
    failed=0
    if message.from_user.id not in SUDO_USERS:
        return
    else:
        wtf = await message.reply("𝑺𝒕𝒂𝒓𝒕𝒊𝒏𝒈 𝑩𝒓𝒐𝒂𝒅𝒄𝒂𝒔𝒕...")
        if not message.reply_to_message:
            await wtf.edit("**__𝑷𝒍𝒆𝒂𝒔𝒆 𝑹𝒆𝒑𝒍𝒚 𝑻𝒐 𝑴𝒆𝒔𝒔𝒂𝒈𝒆 𝑻𝒐 𝑺𝒕𝒂𝒓𝒕 𝑩𝒓𝒐𝒂𝒅𝒄𝒂𝒔𝒕...__**")
            return
        lmao = message.reply_to_message.text
        async for dialog in aditya.iter_dialogs():
            try:
                await aditya.send_message(dialog.chat.id, lmao)
                sent = sent+1
                await wtf.edit(f"𝑩𝒓𝒐𝒂𝒅𝒄𝒂𝒔𝒕𝒊𝒏𝒈 \n\n**𝑺𝒆𝒏𝒕 𝑻𝒐:** `{sent}` 𝑪𝒉𝒂𝒕𝒔 \n**𝑭𝒂𝒊𝒍𝒆𝒅 In:** {failed} chats")
                await asyncio.sleep(3)
            except:
                failed=failed+1
        await message.reply_text(f"𝑮𝒄𝒂𝒔𝒕 𝒔𝒖𝒄𝒄𝒆𝒔𝒔𝒇𝒖𝒍𝒍𝒚 \n\n**𝑺𝒆𝒏𝒕 𝑻𝒐:** `{sent}` 𝑪𝒉𝒂𝒕𝒔 \n**𝑭𝒂𝒊𝒍𝒆𝒅 In:** {failed} Ƈɦɑts")
