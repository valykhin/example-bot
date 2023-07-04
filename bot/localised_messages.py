from string import ascii_letters, digits
import logging.config
import gettext

from config import PRIVACY_POLICY_URL, TERMS_OF_SERVICE_URL, EULA_URL, WEBSITE_URL, HOW_TO_URL

logger = logging.getLogger('bot')

en = gettext.translation('bot', localedir='locales', languages=['en'])
ru = gettext.translation('bot', localedir='locales', languages=['ru'])
__ = en.gettext


class DefaultMessages:
    # general
    COMPATIBLE_CHARS = set(ascii_letters + digits + '-' + '_')
    COMPATIBLE_COMMANDS_CHARS = set(ascii_letters + '1234567890' + ' ' + '-' + '_')

    # commands
    COMMANDS = 'Available commands to use: \n' \
               '/help - to list available commands.\n'
    COMMANDS_NOT_VALID_COMMAND = __('Not recognized command, choose command from list')
    VALID_VALUE_SHOULD_CONTAINS = 'Value should contains only letters, digits and symbols "-", "_".'
    VALUE_NOT_VALID = __('Wrong value. ' + 'Value should contains only letters, digits and symbols "-", "_". ' +
                         'Please enter again.')
    HOW_TO_MESSAGE = 'To know how to use VPN bot send "help".'
    PLEASE_TRY_AGAIN = 'Please try again.'

    # common
    COMPATIBLE_DATE_FORMAT = __('%m/%d/%Y')
    COMPATIBLE_DATETIME_FORMAT = __("%m/%d/%Y %H:%M:%S")
    YES = __('Yes')
    NO = __('No')
    CANCEL = __('Cancel')
    ACTION_CANCELED = __('Action canceled')
    ARE_YOU_SURE = __('Are you sure?')
    CHOOSE_COMMANDS = __('Choose actions from menu below')
    HELP_MESSAGE = __('Send /start command to start using bot.\n' +
                      'Available commands to use: \n'
                      '/help - to list available commands.\n'
                      'For more information follow the link {}\n')
    WELCOME_MESSAGE = __('Welcome to Bot! \n'
                         'Here you can:\n'
                         ' - something\n'
                         'Available commands to use: \n'
                         ' - /help - to list available commands.\n'
                         'Send "help" to know how to use VPN bot. For more information follow the link {}\n')
    COMMON_ERROR_MESSAGE = __('Something goes wrong. Please try again.')
    UNKNOWN_CHAT_MESSAGE = __("I'm sorry, I didn't understand you  =(. To know how to use VPN bot send \"help\".")
    ENTER_NAME_MESSAGE = __('Enter name. ' + 'Value should contains only letters, digits and symbols "-", "_". ' +
                            'Please enter again.'),
    MENU_OPTION_IS_NOT_AVAILABLE_YET = __("I'm sorry but this option is now available for now, please select another.")

    # user settings
    USER_AGREEMENTS_MESSAGE = __("Please read our agreements:\n"
                                 "  - Privacy Policy - {}\n"
                                 "  - Terms Of Service - {}\n"
                                 "  - End User License Agreement - {}\n"
                                 "By clicking the \"Yes\" button and/or by using the bot, the user (\"You\") agree(s) "
                                 "with Privacy Policy, Terms Of Service and End User Agreement License.")
    USER_AGREEMENTS_NOT_VALID_ANSWER = __("Your answer should be \"Yes\" or \"No\".")
    USER_AGREEMENTS_SUCCESS = __("Thank you. These agreements are available on our website: {}")
    USER_SETTINGS_UPDATE_ERROR = __("An error occurred while updating your profile. Please try again.")

    # chat
    CHAT_HI = __("Hi! I'm VPN bot.")
    CHAT_HOW_ARE_YOU = __("How are you?")
    CHAT_HOW_ARE_YOU_ANSWER = __("I'm fine. How are you?")

    # Configs
    USERS_CREATE_CONFIG = __('Create new configuration')
    USERS_CHOOSE_CONFIG = __('Choose configurations from list')
    USERS_CREATE_CONFIG_ERROR = __('An error occurred while creating user. Please try again.')


class Message(DefaultMessages):

    def __init__(self, translations: gettext.translation):
        translations.install()
        _ = translations.gettext
        self.COMPATIBLE_DATE_FORMAT = _(self.COMPATIBLE_DATE_FORMAT)
        self.COMPATIBLE_DATETIME_FORMAT = _(self.COMPATIBLE_DATETIME_FORMAT)
        self.YES = _(self.YES)
        self.NO = _(self.NO)
        self.CANCEL = _(self.CANCEL)
        self.ACTION_CANCELED = _(self.ACTION_CANCELED)
        self.ARE_YOU_SURE = _(self.ARE_YOU_SURE)
        self.CHOOSE_COMMANDS = _(self.CHOOSE_COMMANDS)
        self.COMMANDS_NOT_VALID_COMMAND = _(self.COMMANDS_NOT_VALID_COMMAND)
        self.VALID_VALUE_SHOULD_CONTAINS = _(self.VALID_VALUE_SHOULD_CONTAINS)
        self.VALUE_NOT_VALID = _(self.VALUE_NOT_VALID)
        self.HOW_TO_MESSAGE = _(self.HOW_TO_MESSAGE)
        self.HELP_MESSAGE = _(self.HELP_MESSAGE).format(HOW_TO_URL)
        self.WELCOME_MESSAGE = _(self.WELCOME_MESSAGE).format(HOW_TO_URL)
        self.COMMON_ERROR_MESSAGE = _(self.COMMON_ERROR_MESSAGE)
        self.UNKNOWN_CHAT_MESSAGE = _(self.UNKNOWN_CHAT_MESSAGE)
        self.ENTER_NAME_MESSAGE = _(self.ENTER_NAME_MESSAGE)
        self.PLEASE_TRY_AGAIN = _(self.PLEASE_TRY_AGAIN)
        self.MENU_OPTION_IS_NOT_AVAILABLE_YET = _(self.MENU_OPTION_IS_NOT_AVAILABLE_YET)
        self.USER_AGREEMENTS_MESSAGE = _(self.USER_AGREEMENTS_MESSAGE).format(PRIVACY_POLICY_URL, TERMS_OF_SERVICE_URL,
                                                                              EULA_URL)
        self.USER_AGREEMENTS_NOT_VALID_ANSWER = _(self.USER_AGREEMENTS_NOT_VALID_ANSWER)
        self.USER_AGREEMENTS_SUCCESS = _(self.USER_AGREEMENTS_SUCCESS).format(WEBSITE_URL)
        self.USER_SETTINGS_UPDATE_ERROR = _(self.USER_SETTINGS_UPDATE_ERROR)
        self.CHAT_HI = _(self.CHAT_HI)
        self.CHAT_HOW_ARE_YOU = _(self.CHAT_HOW_ARE_YOU)
        self.CHAT_HOW_ARE_YOU_ANSWER = _(self.CHAT_HOW_ARE_YOU_ANSWER)
        self.USERS_CREATE_CONFIG = _(self.USERS_CREATE_CONFIG)
        self.USERS_CHOOSE_CONFIG = _(self.USERS_CHOOSE_CONFIG)
        self.USERS_CREATE_CONFIG_ERROR = _(self.USERS_CREATE_CONFIG_ERROR)


messages_ru = Message(ru)
messages_en = Message(en)


def get_message(language_code):
    if language_code == 'ru':
        return messages_ru
    else:
        return messages_en
