# First message when starting the bot
GREETING = "Hi! I'm the power hour suggestions bot. Suggest a power hour music video by selecting /suggest."

HELP = GREETING + "\n\n The github for this code is at: [GitHub](https://github.com/MechLizard/PowerHourSuggestions)"

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
SUGGESTION_POST = ("Submission from: <a href=\"tg:// user?id={user_id}\">{user_name}</ a>\n\n"
                   "{URL}")
COMMENT_FROM_SUGGESTOR = "Comment from submitter: {comment}"

# Superuser Commands
COMMAND_INFO_COMMAND = "commands"
BAN_USER_COMMAND = "ban"
UNBAN_USER_COMMAND = "unban"
ENABLE_BOT = "enable bot"
DISABLE_BOT = "disable bot"


# Command responses
USER_BANNED = "That user has been banned."
USER_UNBANNED = "That user has been unbanned."
USER_NOT_BANNED = "That user has not been banned."
BOT_ENABLED = "The bot has been enabled."
BOT_ALREADY_ENABLED = "The bot is already enabled."
BOT_DISABLED = "The bot has been disabled."
BOT_ALREADY_DISABLED = "The bot is already disabled."
ERROR_COULD_NOT_FIND_REPLY_USER = "Error: Could not find the user name in the message you replied to."