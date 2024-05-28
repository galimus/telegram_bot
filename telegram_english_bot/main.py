import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters


lessons = [
    {"title": "Урок 1", "url": "https://youtu.be/I2OGWFVerXg?si=IZq-Ugt_cej61QTL"},
    {"title": "Урок 2", "url": "https://youtu.be/SYHWCn0GqCw?si=YZUWDILnAzwYzAFn"},
    {"title": "Урок 3", "url": "https://youtu.be/OtmUQwPVLko?si=fZQV1MigrZY0FFPT"},
]

users = set()

def save_user(chat_id):
    users.add(chat_id)
    with open("users.json", "w") as f:
        json.dump(list(users), f)

def load_users():
    global users
    try:
        with open("users.json", "r") as f:
            users = set(json.load(f))
    except FileNotFoundError:
        users = set()

def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id
    save_user(chat_id)
    keyboard = [
        [InlineKeyboardButton(lesson["title"], callback_data=lesson["url"]) for lesson in lessons]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"Здравствуйте, {user.first_name}! Я User. Какой урок хотите посмотреть?", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    lesson_url = query.data
    query.edit_message_text(text=f"Вот ваш урок: {lesson_url}")

   
    keyboard = [
        [InlineKeyboardButton(lesson["title"], callback_data=lesson["url"]) for lesson in lessons]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=query.message.chat_id, text='Выберите другой урок:', reply_markup=reply_markup)

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Это бот для предоставления видеоуроков. Вы можете использовать команду /start для начала. Контакты: @astrpv")

def broadcast(update: Update, context: CallbackContext) -> None:
    message = ' '.join(context.args)
    for user in users:
        context.bot.send_message(chat_id=user, text=message)

def main() -> None:
    load_users()
    
  
    token = ""
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler("broadcast", broadcast, Filters.user(username="your_username")))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
