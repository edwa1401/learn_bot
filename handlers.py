from glob import glob
from random import choice
from telegram import Update
from telegram.ext import ContextTypes

from utils import get_smile, play_random_numbers, main_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    context.user_data['emoji'] = get_smile(context.user_data)
    await update.message.reply_text(
        f"Здравствуй пользователь {context.user_data['emoji']}!",
        reply_markup=main_keyboard()
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text
    await update.message.reply_text(f"{text} {context.user_data['emoji']}",
        reply_markup=main_keyboard()
    )

async def guess_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    await update.message.reply_text(message, reply_markup=main_keyboard()
    )

async def sent_cat_picture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cat_photo_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    await context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, 'rb'),
        reply_markup=main_keyboard()
    )

async def user_coordinates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    await update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}!",
        reply_markup=main_keyboard()
    )
