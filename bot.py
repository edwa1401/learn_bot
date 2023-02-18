from emoji import emojize
from glob import glob
import logging
from random import choice, randint
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import settings

# Enable logging
logging.basicConfig(filename='bot.log', level=logging.INFO)
#logging.basicConfig(
#    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
#)
#logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    context.user_data['emoji'] = get_smile(context.user_data)
    await update.message.reply_text(f"Здравствуй пользователь {context.user_data['emoji']}!")
#    await update.message.reply_html(
#        rf"Hi {user.mention_html()}!",
#        reply_markup=ForceReply(selective=True),
#    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text
    await update.message.reply_text(f"{text} {context.user_data['emoji']}")

def get_smile(user_data: dict) -> dict:
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data['emoji']

def play_random_numbers(user_number: int) -> str:
    bot_number = randint(user_number - 10, user_number +10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, мое {bot_number}, вы выиграли"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, мое {bot_number}, ничья"
    else:
        message = f"Ваше число {user_number}, мое {bot_number}, вы проиграли"
    return message

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
    await update.message.reply_text(message)

async def sent_cat_picture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cat_photo_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    await context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, 'rb'))


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(settings.API_KEY).build()

    # on different commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("guess", guess_number))
    application.add_handler(CommandHandler("cat", sent_cat_picture))

    # on non command i.e message - echo the message on Telegram
#    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.TEXT, echo))

    logging.info('Бот стартовал')
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
