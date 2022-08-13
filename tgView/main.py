
import actions as act
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5473222973:AAHnYX5GtYI77gP0Qvm5MFcaTNx_39Uo0KE").build()

    application.add_handler(CallbackQueryHandler(act.callback))

    # Start command 
    # TODO: add more pages
    application.add_handler(CommandHandler("start", act.start))
    application.add_handler(CommandHandler("events", act.start))

    # Run the bot until the user presses Ctrl-C 
    application.run_polling()


if __name__ == "__main__":
    main()
