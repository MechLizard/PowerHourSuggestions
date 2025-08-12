# Power Hour Suggestion Bot

Telegram bot that accepts video suggestions from a user to be sent to one or more admins/power users. 


# Features

Administrative functions:
- Ban/unban suggesters
- List suggestions since the last split
- Split the suggestion history
- Enable/disable the bot.

User functions:
After suggesting a link to a video the user has the option of including a comment.

## Usage
1. Install prerequisites

```
pip install -r requirements.txt
```

2. **Run once to generate default config**

```bash
python main.py
```
3. **Edit `BotConfig.ini`**
   Example:

```ini
[SETUP]
telegram_api_token = 123456:ABC-DEF1234ghIkl-mno57P2Q1R123st11
# The ID of the user(s) that is allowed to give moderator commands and gets suggestions. Can add multiple, each separated by a comma.
super_user_id = [123456789, 987654321]
```

* `telegram_api_token`: Your bot API key from BotFather
* `super_user_id`: Admin IDs from a Telegram info bot
4. **Run the bot**

```bash
python main.py
```