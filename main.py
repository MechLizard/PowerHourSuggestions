from __future__ import annotations
from telegram import Update
from telegram.ext import (
    filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
)

import ConfigHandler
import PowerHourSuggestions

config = ConfigHandler.read_config()
apiToken = config['SETUP']['telegram_api_token']

# Apply token
if apiToken:
    application = ApplicationBuilder().token(apiToken).build()
else:
    raise ValueError("API token is missing or invalid. Check BotConfig.ini and insert it there.")

# == Async Functions == #
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await PowerHourSuggestions.start(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await PowerHourSuggestions.help_command(update, context)

async def suggest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await PowerHourSuggestions.suggest_command(update, context)

async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await PowerHourSuggestions.receive_text(update, context)

async def receive_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await PowerHourSuggestions.button_press(update, context)

# == Main == #
if __name__ == '__main__':
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), receive_text)
    start_handler = CommandHandler('start', start)

    application.add_handler(start_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("suggest", suggest_command))
    application.add_handler(text_handler)
    application.add_handler(CallbackQueryHandler(receive_button_press))

    application.run_polling()
