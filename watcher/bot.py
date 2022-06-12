#placeholder

import config

import logging
from datetime import datetime

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
    ForceReply
)

from telegram.ext import (
    ApplicationBuilder, 
    filters, 
    MessageHandler,  
    CommandHandler,
    CallbackQueryHandler, 
    ContextTypes
)


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")



def main_menu_keyboard():
    keyboard = [
        [
            KeyboardButton('Set location', callback_data='set_location', request_location=True)
        ],
        [
            KeyboardButton('Start polling'),
            KeyboardButton('Stop polling')
        ]
    ]
    return keyboard

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!"
    )

    message = "Please send your location"

    reply_markup = ReplyKeyboardMarkup(main_menu_keyboard())

    await update.effective_message.reply_text(
        message, 
        reply_markup=reply_markup
    )

async def send_update(context: ContextTypes.DEFAULT_TYPE):
    job = context.job

    msg = f'Update({current_time()}) - 30sec: {job.data}'
    await context.bot.send_message(
        job.chat_id, 
        text=msg
    )

def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'USER MSG: {update.message}')
    print(f'DATA: {context.user_data}')
    print(f'CONTEXT(args): {context.args}')

    if 'user_location' not in context.user_data:
        await update.message.reply_text(
            f"Oops! Looks like you haven't set a location yet."
        )
        return

    command = update.message.text
    chat_id = update.effective_message.chat_id

    if command == 'Start polling':
        print('Start polling event')

        job_removed = remove_job_if_exists(str(chat_id), context)

        context.job_queue.run_repeating(
            send_update, 
            interval=30, 
            first=1, 
            chat_id=chat_id, 
            name=str(chat_id),
            data=context.user_data
        )

        msg = ''
        if job_removed:
            msg += 'Reset polling:'
        else:
            msg += 'Initialize polling:'

        msg += f'\n{current_time()}'

        await update.effective_message.reply_text(
            msg
        )
        return

    if command == 'Stop polling':
        print('Stop polling event')

        job_removed = remove_job_if_exists(str(chat_id), context)
        msg = ''
        if job_removed:
            msg += 'Stopped polling:'
        else:
            msg += 'Polling hasnt been started yet:'

        msg += f'\n{current_time()}'

        await update.effective_message.reply_text(
            msg
        )
        return

    await update.message.reply_text(
        f'Unknown command: {update.message.text}'
    )

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.message.chat
    user_name = (chat.first_name, chat.last_name)
    user_location = update.message.location

    context.user_data['user_location'] = user_location
    context.user_data['user_name'] = user_name

    google_maps_url = f'https://www.google.com/maps/place/{user_location.latitude},{user_location.longitude}'

    print(f'LOCATION: {user_name} {user_location.latitude, user_location.longitude}')
    await update.effective_message.reply_text(
        f'{user_name}, you are here {user_location.latitude, user_location.longitude}\n{google_maps_url}'
    )

async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'ECHO: {update.message}')

    print(f'DATA: {context.user_data}')
    print(f'CONTEXT(args): {context.args}')

    await update.message.reply_text(
        f'You said: {update.message.text}'
    )

def main():
    application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start_handler))

    application.add_handler(MessageHandler(filters.LOCATION & ~filters.COMMAND, location_handler))

    application.add_handler(MessageHandler(filters.Regex('^(Start|Stop)\spolling'), main_menu_handler))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_handler))

    application.run_polling()



if __name__ == '__main__':
    print(f'Started {current_time()}')

    main()
