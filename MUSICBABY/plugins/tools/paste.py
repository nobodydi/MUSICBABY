from asyncio import get_running_loop, sleep, TimeoutError
from functools import partial
from MUSICBABY import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import ClientSession
import re
import os
import socket
import aiofiles
import aiohttp
import asyncio
from io import BytesIO

def send_welcome(message):
    BABY.reply_to(message, "Welcome! Send me any code, and I'll paste it to Pastebin for you.")

@MUSICBABY.message_handler(func=lambda message: True)
def paste_to_pastebin(message):
    chat_id = message.chat.id
    code_to_paste = message.text

    try:
        # Create a new paste on Pastebin
        paste_url = pastebin.create_paste(code_to_paste)
        BABY.send_message(chat_id, f"Your code has been pasted to Pastebin! Here is the link:\n{paste_url}")

    except Exception as e:
        BABY.send_message(chat_id, f"An error occurred: {str(e)}")

# Start the bot
if __name__ == "__main__":
    BABY.polling()
