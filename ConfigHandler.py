import configparser
import ast

def get_default_config():
    setup = {
        'telegram_api_token': '',
        'super-user_id': [],
    }
    state = {
        'bot_enabled': True,
    }

    default_config = {'SETUP': setup,
                      'STATE': state}

    return default_config

def create_default_config_file():
    config = configparser.ConfigParser(allow_no_value=True)
    config_info = get_default_config()

    # Copy and convert all the values to strings. ConfigParser requires this
    save_conf = config_info.copy()
    for outer_key, inner_dict in config_info.items():
        save_conf[outer_key] = inner_dict.copy()
        for inner_key, inner_value in inner_dict.items():
            save_conf[outer_key][inner_key] = str(inner_value)

    # SETUP section
    config.add_section('SETUP')
    config.set('SETUP', '# The token you got from Telegram\'s BotFather as a string', None)
    config.set('SETUP', 'TELEGRAM_API_TOKEN', save_conf['SETUP']['telegram_api_token'])
    config.set('SETUP', '# The ID of the user that is allowed to give moderator commands. Can add multiple, each separated by a comma. A list of ints (can be one)', None)
    config.set('SETUP', 'SUPER_USER_ID', save_conf['SETUP']['super_user_id'])

    # STATE section
    config.add_section('STATE')
    config.set('STATE', '# Whether the bot is enabled at the start', None)
    config.set('STATE', 'BOT_ENABLED', save_conf['STATE']['bot_enabled'])

    with open('BotConfig.ini', 'w') as configfile:
        config.write(configfile)

def read_config():
    config_dict = {}
    config = configparser.ConfigParser()

    # Read in BotConfig.ini. If it doesn't exist get a default one.
    try:
        with open('BotConfig.ini') as f:
            config.read_file(f)
        for section in config.sections():
            config_dict[section] = dict(config[section])
    except IOError:
        create_default_config_file()

    config.read('BotConfig.ini')

    # Convert the strings from the .ini in to their appropriate variable types
    for outer_key, inner_dict in config_dict.items():
        for inner_key, inner_value in inner_dict.items():
            try:
                # Try to convert the string to a number or bool
                inner_dict[inner_key] = ast.literal_eval(inner_value)
            except ValueError:
                # If fails, that means it was already the correct value
                pass
            # This is there because the format of the api token can cause a syntax error
            except SyntaxError:
                pass

    return config_dict
