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

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the PasteBot! Send /paste to save a text snippet.')

# Define the paste command
def paste(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    text = ' '.join(context.args)

    if not text:
        update.message.reply_text('Please provide text to paste. Usage: /paste <your text>')
        return

    pastes[chat_id] = text
    update.message.reply_text('Your text has been pasted. Use /get to retrieve it.')

# Define the get command
def get(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if chat_id in pastes:
        text = pastes[chat_id]
        update.message.reply_text(f'Your pasted text:\n\n{text}')
    else:
        update.message.reply_text('No pasted text found. Use /paste to save a text snippet.')

# Define the echo handler for handling regular messages
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("I don't understand that command. Use /start, /paste, or /get.")

def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("paste", paste, pass_args=True))
    dp.add_handler(CommandHandler("get", get))
    
    # Register an echo handler for regular messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
