import pickle
from typing import Dict, Union, Set
import re

from telegram import Update, Message, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

import Responses


async def super_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, state_cf, ban_list: Set[int]) -> bool:
    """ Takes a command sent by a superuser. Check whether the messages match a superuser command. If so, run that command.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user
        :param state_cf: Dict of configuration settings relating to the state of the script.
        :param ban_list: Set of user IDs that are banned.

        :returns: A bool indicating whether the message matches a command.
    """

    # Reply command
    if update.message.reply_to_message is not None:
        reply_message = update.message.reply_to_message

        # Get the user mentioned in the reply
        user_id = get_user_from_text(reply_message.text_html)

        if user_id is None:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=Responses.ERROR_COULD_NOT_FIND_REPLY_USER)
            return True
        elif await ban_unban(update, context, command, user_id, ban_list):
            return True
        elif await enable_disable_bot(update, context, command):
            return True

    return False


# TODO user_commands
async def user_text(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, user_id: int, active_suggestors: Dict[int, str]) -> bool:
    """ Takes a command sent by a superuser. Check whether the messages match a superuser command. If so, run that command.

        :param update: Update object containing the sent message.
        :param context: Object containing the bot interface for the current chat.
        :param command: The text command sent by the user
        :param user_id: The user ID
        :param active_suggestors: Dict of active suggestors.

        :returns: A bool indicating whether the message matches a command.
    """

    if user_id not in active_suggestors:
        return False

    # If there is no link recorded for the user yet.
    if active_suggestors[user_id] == "":
        # TODO Get the first link, remove tracking stuff. Then save to active_suggestors[user_id]
        # TODO Check if the link was sent before.
        keyboard = [
            [InlineKeyboardButton(Responses.SUGGESTION_YES_BUTTON, callback_data=Responses.SUGGESTION_YES_CALLBACK_DATA)],
            [InlineKeyboardButton(Responses.SUGGESTION_NO_BUTTON, callback_data=Responses.SUGGESTION_NO_CALLBACK_DATA)],
        ]
        reply_buttons = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=Responses.SUGGESTION_COMMENT, reply_markup=reply_buttons)

        return True

    # If there is already a link sent by the user and it's still active then the user is making a comment.
    # TODO: Send link to superuser(s)



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
        return True

    # unban
    if command == Responses.UNBAN_USER_COMMAND:
        if user_id in ban_list:
            text = Responses.USER_NOT_BANNED
        else:
            text = Responses.USER_BANNED
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return True

    return False

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
