
import actions as act
import text as msg
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    CallbackQueryHandler,
    ConversationHandler,
)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5473222973:AAHnYX5GtYI77gP0Qvm5MFcaTNx_39Uo0KE").build()
    application.add_handler(CallbackQueryHandler(act.callback))

    # Start command 
    # TODO: add more pages
    # Edit registration screen
    application.add_handler(CommandHandler("start", act.start))

    # Logic to start as Company ()
    application.add_handler(CommandHandler("become_executor", act.executor))
    # Company logic 
    application.add_handler(CommandHandler("add_event", act.addevent))
    application.add_handler(CommandHandler("events", act.events))
    application.add_handler(CommandHandler("add_tag", act.addtag))
    application.add_handler(CommandHandler("share", act.share))

    # User logic
    application.add_handler(CommandHandler("appointments", act.appoint))
    application.add_handler(CommandHandler("shared", act.shared))


    # Run the bot until the user presses Ctrl-C 
    application.run_polling()


if __name__ == "__main__":
    main()
