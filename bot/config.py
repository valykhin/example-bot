import os
import logging.config

LOGGER_CONFIGURATION_FILE = os.environ.get('LOGGER_CONFIGURATION_FILE', 'logging.conf')
logging.config.fileConfig(LOGGER_CONFIGURATION_FILE)

logger = logging.getLogger('bot')
logger.info('Logger configuration loaded: {}'.format(LOGGER_CONFIGURATION_FILE))


def get_secret_or_env(env_name, default_value='', env_secret_file=''):
    result = ''
    if env_secret_file == '':
        env_secret_file = env_name + "_FILE"
    if not os.environ.get(env_name, ''):
        logger.info('{} variable is empty'.format(env_name))
        secret_file = os.environ.get(env_secret_file, '')
        if os.path.exists(secret_file):
            with open(secret_file, 'r', encoding="utf-8") as f:
                for line in f:
                    result = line.strip()
    else:
        result = os.environ.get(env_name)
    if not result:
        result = default_value
    return result


def get_bot_token():
    bot_token = ''
    if not os.environ.get('BOT_TOKEN', ''):
        logger.info('BOT_TOKEN variable is empty')
        token_vpn_file = os.environ.get("VPN_BOT_TOKEN_FILE")
        if os.path.exists(token_vpn_file):
            with open(token_vpn_file, 'r', encoding="utf-8") as f:
                for line in f:
                    bot_token = line.strip()
        else:
            raise FileNotFoundError('File {} not exists'.format(token_vpn_file))
    else:
        bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        raise AttributeError('Bot token is empty')
    return bot_token


def get_provider_token():
    token = ''
    if not os.environ.get('PAYMENT_PROVIDER_TOKEN', ''):
        logger.info('PAYMENT_PROVIDER_TOKEN variable is empty')
        token_file = os.environ.get("PAYMENT_PROVIDER_TOKEN_FILE")
        if os.path.exists(token_file):
            with open(token_file, 'r', encoding="utf-8") as f:
                for line in f:
                    token = line.strip()
        else:
            raise FileNotFoundError('File {} not exists'.format(token_file))
    else:
        token = os.environ.get("PAYMENT_PROVIDER_TOKEN")
    if not token:
        raise AttributeError('Bot payment provider token is empty')
    return token


BOT_TOKEN = get_bot_token()
CORE_SERVER_API_URL = os.environ.get("CORE_API_URL", "http://127.0.0.1:8000/api")
PAYMENT_PROVIDER_TOKEN = get_provider_token()
PRIVACY_POLICY_URL = os.environ.get('PRIVACY_POLICY_URL', 'https://example.com/privacy-policy')
TERMS_OF_SERVICE_URL = os.environ.get('TERMS_OF_SERVICE_URL', 'https://example.com/terms-of-service')
EULA_URL = os.environ.get('EULA_URL', 'https://example.com/eula')
WEBSITE_URL = os.environ.get('WEBSITE_URL', 'https://example.com/')
HOW_TO_URL = os.environ.get('HOW_TO_URL', 'https://example.com/how-to-use')
BASIC_AUTH_CORE_USER = get_secret_or_env('BASIC_AUTH_CORE_USER', 'core')
BASIC_AUTH_CORE_PASSWORD = get_secret_or_env('BASIC_AUTH_CORE_PASSWORD', 'typxsyCstN')
