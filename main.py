import ptbot
from dotenv import load_dotenv
import os
from pytimeparse import parse


def render_progressbar(total, iteration, prefix='',
                       suffix='', length=30, fill='█', zfill='░'
                       ):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, total_seconds, chat_id, message_id, bot):
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


def countdown_callback(secs_left, total_seconds, chat_id, message_id):
    notify_progress(secs_left, total_seconds, chat_id, message_id, bot)


def main(chat_id, question):
    seconds = parse(question)
    message_id = bot.send_message(chat_id, 'Запускаю таймер')
    bot.create_countdown(
                         seconds,
                         lambda secs_left: countdown_callback(
                                                              secs_left,
                                                              seconds,
                                                              chat_id,
                                                              message_id
                                                              )
                         )
    bot.create_timer(
                     seconds,
                     lambda: choose(chat_id, "Время вышло!")
                     )


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(lambda chat_id, question: main(chat_id, question))
    bot.run_bot()
