#placeholder

import config

import logging
from datetime import datetime

from telegram import Update
from telegram.ext import ApplicationBuilder, filters, MessageHandler,  CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'ECHO: {update.message.text}')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def main():
    application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    application.run_polling()



if __name__ == '__main__':
    print(f'Started {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    main()
