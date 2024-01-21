from asyncio import get_running_loop, sleep, TimeoutError
from functools import partial
from MUSICBABY import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  # Import Update and CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Your Pastebin API key
PASTEBIN_API_KEY = 'YOUR_PASTEBIN_API_KEY'

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Send me a message, and I will create a Pastebin link for it.')

# Function to handle text messages
def handle_text(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    # Make a request to Pastebin API to create a new paste
    data = {
        'api_dev_key': PASTEBIN_API_KEY,
        'api_paste_data': text,
        'api_paste_private': '1',  # 1: Private, 0: Public
        'api_paste_name': 'Telegram Message',
        'api_paste_expire_date': '1D'  # Paste expiration (1 day in this example)
    }

    response = requests.post('https://pastebin.com/api/api_post.php', data=data)

    if response.ok:
        paste_url = response.text
        update.message.reply_text(f'Your Pastebin link: {paste_url}')
    else:
        update.message.reply_text('Error creating Pastebin link. Please try again.')

# Main function to start the bot
def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))

    # Register message handler for all text messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == '__main__':
    main()
