#placeholder

import config

import logging
from datetime import datetime

from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def echo(update: Update, context: CallbackContext):
    print(f'ECHO: {update.message.text}')
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def main():
    updater = Updater(token=config.TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()

    updater.stop()



if __name__ == '__main__':
    print(f'Started {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    try:
        main()
    except KeyboardInterrupt as kie:
        print(f'Killed: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')