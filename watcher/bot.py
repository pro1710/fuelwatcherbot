#placeholder

import config
import logging
import helpers
import traceback
from datetime import datetime

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update
)

from telegram.ext import (
    ApplicationBuilder, 
    filters, 
    MessageHandler,  
    CommandHandler,
    ContextTypes
)

class Command:
    START = 'START'
    STOP = 'STOP'
    FORCE_UPDATE = 'FORCE UPDATE'

def main_menu_keyboard():
    keyboard = [
        [
            KeyboardButton('Set location', request_location=True),
            KeyboardButton(Command.FORCE_UPDATE)
        ],
        [
            KeyboardButton(Command.START),
            KeyboardButton(Command.STOP)
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

    # TODO: rework

    msg = f'UPDATE({helpers.current_time()})\n'
    msg += '\n'.join(helpers.get_closest('./data/wog/last.pkl', job.data['user_location']))
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
    if 'user_location' not in context.user_data:
        logging.info(f'Polling event without location')

        await update.message.reply_text(
            f"Oops! Looks like you haven't set a location yet."
        )
        return

    command = update.message.text
    chat_id = update.effective_message.chat_id

    if command == Command.START:
        logging.info('Start polling event')

        job_removed = remove_job_if_exists(str(chat_id), context)

        context.job_queue.run_repeating(
            send_update, 
            interval=30*60, 
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

        msg += f'\n{helpers.current_time()}'

        await update.effective_message.reply_text(
            msg
        )
        return

    if command == Command.STOP:
        logging.info('Stop polling event')

        job_removed = remove_job_if_exists(str(chat_id), context)
        msg = ''
        if job_removed:
            msg += 'Stopped polling:'
        else:
            msg += 'Polling hasnt been started yet:'

        msg += f'\n{helpers.current_time()}'

        await update.effective_message.reply_text(
            msg
        )
        return

    if command == Command.FORCE_UPDATE:
        msg = f'UPDATE({helpers.current_time()})\n'
        msg += '\n'.join(helpers.get_closest('./data/wog/last.pkl', context.user_data['user_location']))
        await update.effective_message.reply_text(
            text=msg
        )
        return

    await update.message.reply_text(
        f'Unknown command: {update.message.text}'
    )

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.message.chat
    location = update.message.location
    context.user_data['user_location'] = {
        'latitude': location.latitude, 
        'longitude': location.longitude
    }
    context.user_data['user_name'] = {
        'first_name': chat.first_name, 
        'last_name': chat.last_name
    }

    user_name = f'{chat.first_name} {chat.last_name}'
    user_location = f'{location.latitude},{location.longitude}' 

    logging.info(f'Set new location for {user_name} {user_location}')

    google_maps_url = f'https://www.google.com/maps/place/{user_location}'

    await update.effective_message.reply_text(
        f'{user_name}, you are here {user_location}\n{google_maps_url}'
    )

async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'ECHO: {update.message}')

    print(f'DATA: {context.user_data}')
    print(f'CONTEXT(args): {context.args}')

    await update.message.reply_text(
        f'You said: {update.message.text}'
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:

    logging.error(msg="Exception while handling an update:", exc_info=context.error)
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)

    print("\n".join(tb_list))

def main():
    application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start_handler))
    application.add_handler(MessageHandler(filters.LOCATION & ~filters.COMMAND, location_handler))
    application.add_handler(MessageHandler(filters.Regex(f'^({Command.START}|{Command.STOP}|{Command.FORCE_UPDATE})$'), main_menu_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_handler))

    application.add_error_handler(error_handler)

    application.run_polling()

if __name__ == '__main__':
    helpers.prepare_logger('./log/bot.log')
    logging.info(f'Started')
    print(f'Started: {helpers.current_time()}')
    main()
