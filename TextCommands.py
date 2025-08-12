import pickle
from typing import Dict, Union, Set
import re

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
import yt_dlp

import Responses
import PowerHourSuggestions
import suggestion


async def super_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, state_cf, ban_list: Set[int],
                             active_suggesters: Dict[int, suggestion], suggestion_list: set[suggestion]) -> bool:
    """ Takes a command sent by a superuser. Check whether the messages match a superuser command. If so, run that command.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user
        :param state_cf: Dict of configuration settings relating to the state of the script.
        :param ban_list: Set of user IDs that are banned.
        :param active_suggesters: Dict of suggestions that the bot is interacting with a user for.
        :param suggestion_list: Dict of suggestions since the last wipe.

        :returns: A bool indicating whether the message matches a command.
    """

    # Reply command
    if update.message.reply_to_message is not None:
        reply_message = update.message.reply_to_message

        # Get the user mentioned in the reply
        reply_user_id = get_user_from_text(reply_message.text_html)

        if reply_user_id is None:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=Responses.ERROR_COULD_NOT_FIND_REPLY_USER)
            return True
        elif await ban_unban(update, context, command, reply_user_id, ban_list):
            return True
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=Responses.ERROR_COMMAND_NOT_RECOGNIZED)
            return True

    if await enable_disable_bot(update, context, command, state_cf):
        return True
    if await split(update, context, command):
        return True
    if await list_suggestions(update, context, command, suggestion_list):
        return True
    # Check if the command is a user command and not an admin command.
    if await user_text(update, context, update.message.from_user.id, active_suggesters, suggestion_list):
        return True

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=Responses.ERROR_COMMAND_NOT_RECOGNIZED)
    return True


async def user_text(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int,
                    active_suggesters: Dict[int, suggestion], suggestion_list: set[suggestion]) -> bool:
    """ Takes a command sent by a superuser. Check whether the messages match a superuser command. If so, run that command.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param user_id: The user ID
        :param active_suggesters: Dict of active suggesters.
        :param suggestion_list: Dict of suggestions since the last wipe.

        :returns: A bool indicating whether the message matches a command.
    """

    if user_id not in active_suggesters:
        return False

    # If there is no link recorded for the user yet.
    if active_suggesters[user_id].url is None:

        url = get_link_from_message(update)
        if url is None:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=Responses.SUGGESTION_NO_LINK)
            return True

        # TODO Remove tracking information?
        # TODO Check if the link was sent before?
        active_suggesters[user_id].url = url

        active_suggesters[user_id].video_title = get_youtube_video_title(url)

        keyboard = [
            [InlineKeyboardButton(Responses.SUGGESTION_YES_BUTTON, callback_data=Responses.SUGGESTION_YES_CALLBACK_DATA)],
            [InlineKeyboardButton(Responses.SUGGESTION_NO_BUTTON, callback_data=Responses.SUGGESTION_NO_CALLBACK_DATA)],
        ]
        reply_buttons = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=Responses.SUGGESTION_COMMENT, reply_markup=reply_buttons)

        return True

    # If there is already a link sent by the user, and it's still active then the user is making a comment.
    comment = update.message.text
    active_suggesters[user_id].comment = comment
    await PowerHourSuggestions.forward_to_superuser(context, update.message.from_user.id,
                                                    update.message.chat.username, comment)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=Responses.SUGGESTION_COMPLETE)
    suggestion_list.add(active_suggesters[user_id])
    del active_suggesters[user_id]
    return True



async def ban_unban(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, user_id:int, ban_list: Set[int]) -> bool:
    """ Reply command. Ban (set user's sticker limit to 0) and reset (set user's sticker count to 0) commands.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param user_id: The current user ID the superuser is replying to.
        :param ban_list: Set of user IDs that are banned.

        :returns: A bool indicating whether the message triggers this function.
    """

    # ban
    if command == Responses.BAN_USER_COMMAND:
        ban_list.add(user_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=Responses.USER_BANNED)
        pickle.dump(ban_list, open("ban_list.p", "wb"))
        return True

    # unban
    if command == Responses.UNBAN_USER_COMMAND:
        if user_id not in ban_list:
            text = Responses.USER_NOT_BANNED
        else:
            text = Responses.USER_UNBANNED
            ban_list.remove(user_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        pickle.dump(ban_list, open("ban_list.p", "wb"))
        return True

    return False

async def split(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str,) -> bool:
    """ Turns the bot on or off. Superuser commands can still be sent, but the bot will not respond anything else.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.

        :returns: A bool indicating whether the message triggers this function.
    """

    if command != Responses.SPLIT_COMMAND:
        return False

    # Ask the user to confirm whether they meant to split the list history.
    keyboard = [
        [InlineKeyboardButton(Responses.SU_BUTTON_SPLIT_YES, callback_data=Responses.SU_BUTTON_YES_SPLIT_CALLBACK_DATA)],
        [InlineKeyboardButton(Responses.SU_BUTTON_SPLIT_NO, callback_data=Responses.SU_BUTTON_NO_SPLIT_CALLBACK_DATA)],
    ]
    reply_buttons = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=Responses.SPLIT_CONFIRMATION_REQUEST,
                                   reply_markup=reply_buttons)

    return True

async def list_suggestions(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, suggestion_list: set[suggestion]) -> bool:
    """ Turns the bot on or off. Superuser commands can still be sent, but the bot will not respond anything else.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param suggestion_list: Dict of suggestions since the last wipe.

        :returns: A bool indicating whether the message triggers this function.
    """
    if command != Responses.LIST_COMMAND:
        return False

    text = ""
    if suggestion_list:
        for suggest in suggestion_list:
            text += Responses.LIST_USERNAME.format(user_id=suggest.id, user_name=suggest.username)
            if suggest.video_title:
                text += "\n" + Responses.LIST_VIDEO_TITLE.format(video_title=suggest.video_title)
            text += "\n" + Responses.LIST_URL.format(URL=suggest.url)
            if suggest.comment is not None:
                text += "\n" + Responses.LIST_COMMENT.format(comment=suggest.comment)
            text += "\n\n"
    else:
        text = Responses.LIST_EMPTY

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)


    return True

async def enable_disable_bot(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, state_cf) -> bool:
    """ Turns the bot on or off. Superuser commands can still be sent, but the bot will not respond anything else.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user.
        :param state_cf: Dict of configuration settings relating to the state of the script.

        :returns: A bool indicating whether the message triggers this function.
    """

    # Turn off bot
    if command == Responses.DISABLE_BOT:
        if state_cf['bot_enabled']:
            text = Responses.BOT_DISABLED
        else:
            text = Responses.BOT_ALREADY_DISABLED
        state_cf['bot_enabled'] = False
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True

    # Turn on bot
    if command == Responses.ENABLE_BOT:
        if state_cf['bot_enabled']:
            text = Responses.BOT_ALREADY_ENABLED
        else:
            state_cf['bot_enabled'] = True
            text = Responses.BOT_ENABLED

        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True
    
    return False

def get_user_from_text(message_text: str) -> Union[int, None]:
    """ Gets the user_id from an HTML text mention.
        Used to get the user ID from a message.

        :param message_text: Message text to parse.

        :returns: User ID as int or None
    """
    
    if message_text is None:
        return None

    match = re.search(r'id=(\d+)', message_text)

    if match:
        return int(match.group(1))
    return None

def get_link_from_message(update: Update) -> Union[str, None]:
    """ Gets the first link from a message.

        :param update: Update object containing the sent message.

        :returns: The first link or None
    """
    message = update.message

    if message and message.entities:
        for entity in message.entities:
            if entity.type == MessageEntity.URL:
                url = message.parse_entity(entity)
                return url

    return None

def get_youtube_video_title(url: str) -> str | None:
    ydl_opts = {
        'quiet': True,  # Suppress console output from yt-dlp
        'no_warnings': True,  # Suppress warnings
        'extract_flat': True,  # Only extract basic information, no full download
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return info_dict.get('title', None)
    except Exception as e:
        return None
