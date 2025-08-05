from __future__ import annotations
import pickle
import logging
from datetime import (datetime, timedelta)
from typing import (Dict, Union, List)
import random
from threading import Thread

from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup, Sticker, PhotoSize)
from telegram.constants import ParseMode
from telegram.ext import (ContextTypes, ApplicationBuilder, Application)

import ConfigHandler
import Responses
import TextCommands

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

config = ConfigHandler.read_config()
setup_cf = config['SETUP']
state_cf = config['STATE']

ban_list: set[int] = set() # User ids are stored as an int.
active_suggesters: Dict[int, str] = {} # [(User ID), (the link the user sent, if they sent it yet)]

# Check if there is a previously saved user list
try:
    with open("ban_list.p", "rb") as file:
        users = pickle.load(file)
except FileNotFoundError:
    print("No ban_list.p found. Creating new ban list.")

bot_start_time = datetime.now()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Greets the user and gives instructions on how to use the bot.

    :param update: Update object containing the sent message.
    :param context: Object containing the bot interface for the current chat.
    """

    if not state_cf['bot_enabled']:
        return
    text = Responses.GREETING
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Triggers on \help.
    Replies to the user with basic functionality of the bot, github link, and how many stickers they have left.

    :param update: Update object containing the sent message.
    :param context: Object containing the bot interface for the current chat.
    """

    if not state_cf['bot_enabled']:
        return
    text = Responses.HELP
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def suggest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Triggers on \suggest.
    Saves the user's ID to represent that the user is actively suggesting a link.

    :param update: Update object containing the sent message.
    :param context: Object containing the bot interface for the current chat.
    """

    if not state_cf['bot_enabled']:
        return
    if update.message.from_user.id in ban_list:
        return

    active_suggesters[update.effective_chat.id] = ""

    text = Responses.SUGGESTION_LINK
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Handles incoming text messages and commands from users and superusers.

    :param update: Update object containing the sent message.
    :param context: Object containing the bot interface for the current chat.
    """

    global ban_list

    message_text = update.message.text
    # Superuser commands
    if update.message.from_user.id in setup_cf['super_user_id']:
        if await TextCommands.super_user_command(update, context, message_text, state_cf, ban_list):
            return

    # Normal user commands
    if not state_cf['bot_enabled']:
        return

    if update.message.from_user.id in ban_list:
        return

    await TextCommands.user_text(update, context, message_text, update.message.from_user.id, active_suggesters)


async def button_press(update, context):
    """ Triggers when a button presented by the bot is pressed.

    :param update: Update object containing the sent message.
    :param context: Object containing the bot interface for the current chat.
    """

    query = update.callback_query
    await query.answer()

    # User hits "Yes" when prompted if they want to leave a comment.
    if query.data == Responses.SUGGESTION_YES_CALLBACK_DATA:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=Responses.SUGGESTION_COMMENT)

    # User hits "No" when prompted if they want to leave a comment.
    if query.data == Responses.SUGGESTION_YES_CALLBACK_DATA:
        await forward_to_superuser(context, update.message.from_user.id, update.message.chat.username)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=Responses.SUGGESTION_COMPLETE)


async def forward_to_superuser(context: ContextTypes.DEFAULT_TYPE, current_user_id: int,
                               current_user_name: str, comment=""):
    """ Sends suggestion to the superuser(s).

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param current_user_id: The suggester's ID.
        :param current_user_name: The name of the current user.
        :param comment: Optional comment for the superuser(s) about the link.
    """

    global active_suggesters
    if current_user_id not in active_suggesters:
        return

    superuser_text = Responses.SUGGESTION_POST.format(user_name=current_user_name, user_id=current_user_id,
                                                      URL=active_suggesters[current_user_id])
    for super_id in setup_cf['super_user_id']:
        if comment != "":
            superuser_text += "\n\n" + Responses.COMMENT_FROM_SUGGESTOR.format(comment=comment)

        await context.bot.send_message(chat_id=super_id, text=superuser_text, parse_mode=ParseMode.HTML)
