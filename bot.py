import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from handlers import guess_number, echo, start, sent_cat_picture, user_coordinates
import settings

# Enable logging
logging.basicConfig(filename='bot.log', level=logging.INFO)
#logging.basicConfig(
#    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
#)
#logger = logging.getLogger(__name__)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(settings.API_KEY).build()

    # on different commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("guess", guess_number))
    application.add_handler(CommandHandler("cat", sent_cat_picture))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.Regex('^(Прислать котика)$'), sent_cat_picture))
    application.add_handler(MessageHandler(filters.LOCATION, user_coordinates))
    application.add_handler(MessageHandler(filters.TEXT, echo))

    logging.info('Бот стартовал')
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
