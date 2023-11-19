import requests
from os import getenv

TELEGRAM_TOKEN = '6542037151:AAFvnsJcpvpVGiYxm4gAeeJl2k4p9EAyYtg'
TELEGRAM_MAIN_URL = 'https://api.telegram.org/bot'


def telegram_bot_message(message, chat_id):

    send_text = f'{TELEGRAM_MAIN_URL}{TELEGRAM_TOKEN}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}'
    response = requests.get(send_text)
    return response.json()


if __name__ == '__main__':
    # test = telegram_bot_message("Testing Telegram bot 559773959", 5194882396)
    test = telegram_bot_message("Testing Telegram bot 559773959", 559773959)

    print(test)
