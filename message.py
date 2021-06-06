import config.message_config as message_config
import requests
from typing import Final


class MessageFactory:
    TELEGRAM_BOT_CHAT_ID: Final = message_config.TELEGRAM_BOT_CHAT_ID
    TELEGRAM_BOT_SECURITIES_INVESTMENT_CHAT_ID: Final = message_config.TELEGRAM_BOT_SECURITIES_INVESTMENT_CHAT_ID
    TEST_TELEGRAM_BOT_CHAT_ID: Final = message_config.TEST_TELEGRAM_BOT_CHAT_ID
    TEST_MODEL = message_config.TEST_MODEL

    @staticmethod
    def get_instance(chat_id):
        if MessageFactory.TEST_MODEL:
            chat_id = MessageFactory.TEST_TELEGRAM_BOT_CHAT_ID
        return Message(chat_id)


class Message:
    def __init__(self, chat_id):
        self._chat_id = chat_id

    def send_msg(self, send_message):
        if not send_message == '':
            url = message_config.TELEGRAM_BOT_URL + "sendMessage"
            my_params = {'chat_id': self._chat_id,
                         'parse_mode': 'html',
                         'text': send_message
                         }

            r = requests.get(url, params=my_params)
