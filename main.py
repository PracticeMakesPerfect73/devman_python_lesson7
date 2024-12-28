import ptbot
from dotenv import load_dotenv
import os
from pytimeparse import parse

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')


def render_progressbar(total, iteration, prefix='',
                       suffix='', length=30, fill='█', zfill='░'
                       ):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, total_seconds, chat_id, message_id):
    progress = total_seconds - secs_left
    progress_bar = render_progressbar(total_seconds,
                                      progress,
                                      prefix='',
                                      suffix='',
                                      length=30
                                      )
    bot.update_message(chat_id,
                       message_id,
                       f"Осталось {secs_left} секунд\n{progress_bar}"
                       )


def choose(chat_id, message):
    bot.send_message(chat_id, message)


def main(chat_id, question):
    seconds = parse(question)
    message_id = bot.send_message(chat_id, 'Запускаю таймер')

    def countdown_callback(secs_left):
        notify_progress(secs_left, seconds, chat_id, message_id)

    bot.create_countdown(seconds, countdown_callback)
    bot.create_timer(seconds, choose,
                     chat_id=chat_id,
                     message="Время вышло!"
                     )


if __name__ == '__main__':
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(main)
    bot.run_bot()
