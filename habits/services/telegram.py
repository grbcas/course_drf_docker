import requests
import os
from dotenv import load_dotenv
import telebot



load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_MAIN_URL = os.getenv('TELEGRAM_MAIN_URL')



def telegram_bot_message(message, chat_id):

    send_text = f'{TELEGRAM_MAIN_URL}{TELEGRAM_TOKEN}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}'
    response = requests.get(send_text)
    return response.json()


def telebot_send(message, chat_id):
    bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN
    bot.send_message(chat_id, message)


if __name__ == '__main__':
    # test = telegram_bot_message("Testing Telegram bot 559773959")
    # test = telegram_bot_message("Manual test Telegram bot 559773959", '559773959')
    test = telebot_send("Manual test Telegram bot 559773959", '559773959')
