# Superuser Commands
BAN_USER_COMMAND = "ban"
UNBAN_USER_COMMAND = "unban"
ENABLE_BOT = "enable bot"
DISABLE_BOT = "disable bot"
SPLIT_COMMAND = "split"
LIST_COMMAND = "list"

# First message when starting the bot
GREETING = "Hi! I'm the power hour suggestions bot. Suggest a power hour music video by selecting /suggest."

HELP = GREETING + "\n\n The github for this code is at: [GitHub](https://github.com/MechLizard/PowerHourSuggestions)"
HELP_SUPERUSER = f"""
You are an admin. Here are the commands you can use:

Reply Commands (Reply to a suggestion to apply these commands to a user):
\"{BAN_USER_COMMAND}\" - Bans the user.
\"{UNBAN_USER_COMMAND}\" - Unbans the user.

General Commands:
\"{LIST_COMMAND}\" - Lists all videos since the last {SPLIT_COMMAND} command. 
\"{SPLIT_COMMAND}\" - Creates a split for the {LIST_COMMAND} command. {LIST_COMMAND} commands will only show videos sent from now on once used. 
\"{ENABLE_BOT}\" - Enables the bot.
\"{DISABLE_BOT}\" - Disables the bot."
"""

SU_BUTTON_SPLIT_YES = "YES"
SU_BUTTON_SPLIT_NO = "NO"
SU_BUTTON_YES_SPLIT_CALLBACK_DATA = "su_button_split_yes"
SU_BUTTON_NO_SPLIT_CALLBACK_DATA = "su_button_split_no"
SPLIT_CONFIRMATION_REQUEST = "Are you sure you want to split the suggestion history? This will list all suggestions sent from the last split and then wipe the suggestion history."
SPLIT_CANCELLED = "Split cancelled."
SPLIT_COMPLETED = "Suggestion history wiped. Starting new list."

LIST_EMPTY = "There have been no suggestions sent since the last split."
LIST_ENTRY = ("From: <a href=\"tg://user?id={user_id}\">{user_name}</a>\n\n"
              "{URL}")
LIST_COMMENT = "Comment: {comment}"

# Submitting a suggestion
SUGGESTION_LINK = "Okay. Send me JUST the link to the video. You can send a comment about it after."
SUGGESTION_ALREADY_SUBMITTED = "Looks like that link was already submitted!"
SUGGESTION_COMMENT = "Got it. Would you like to tell the organizer anything about this suggestion?"
SUGGESTION_YES_BUTTON = "Yes. I have a comment about it."
SUGGESTION_YES_CALLBACK_DATA = "yes_comment_button"
SUGGESTION_NO_BUTTON = "No. Just submit the link."
SUGGESTION_NO_CALLBACK_DATA = "no_comment_button"
SUGGESTION_COMPLETE = "Suggestion submitted. Thank you!"
SUGGESTION_NO_LINK = "No link found in message. Please try again."

# Posting the suggestion
SUGGESTION_POST = ("Submission from: <a href=\"tg://user?id={user_id}\">{user_name}</a>\n\n"
                   "{URL}")
COMMENT_FROM_SUGGESTOR = "Comment from submitter: {comment}"


# Command responses
USER_BANNED = "That user has been banned."
USER_UNBANNED = "That user has been unbanned."
USER_NOT_BANNED = "That user was not on the ban list."
BOT_ENABLED = "The bot has been enabled."
BOT_ALREADY_ENABLED = "The bot is already enabled."
BOT_DISABLED = "The bot has been disabled."
BOT_ALREADY_DISABLED = "The bot is already disabled."
ERROR_COULD_NOT_FIND_REPLY_USER = "Error: Could not find the user name in the message you replied to."
ERROR_COMMAND_NOT_RECOGNIZED = "I don't recognize that command. Type /help to get a list of commands."