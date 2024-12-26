import ptbot
from dotenv import load_dotenv
import os
from pytimeparse import parse
load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')
bot = ptbot.Bot(TG_TOKEN)

def notify_progress(secs_left, chat_id, message_id):
    bot.update_message(chat_id, message_id, secs_left)

def choose(chat_id, message):
    bot.send_message(chat_id, message)

def wait(chat_id, question):
    message_id = bot.send_message(chat_id, 'Запускаю таймер')
    seconds = parse(question)
    bot.create_countdown(seconds, notify_progress, chat_id, message_id)
    bot.create_timer(seconds, choose, chat_id=chat_id, message="Время вышло!")
bot.reply_on_message(wait)
bot.run_bot()
