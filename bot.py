import logging

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
    await update.message.reply_text('Здравствуй пользователь')
#    await update.message.reply_html(
#        rf"Hi {user.mention_html()}!",
#        reply_markup=ForceReply(selective=True),
#    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(settings.API_KEY).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
#    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.TEXT, echo))

    logging.info('Бот стартовал')
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
