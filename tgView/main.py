
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
    application.add_handler(CommandHandler("start", act.start))

    # Logic to start as Company ()
    # Become Executor handler
    executor = ConversationHandler(
        entry_points=[CommandHandler("become_executor", act.executor)],
        states={
            act.AGREE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, 
                    act.exec_state,
                ),
            ],
        },
        fallbacks=[CommandHandler("cancel", act.cancel)],
    )

    application.add_handler(executor)

    application.add_handler(CommandHandler("add_event", act.addevent))

    # Run the bot until the user presses Ctrl-C 
    application.run_polling()


if __name__ == "__main__":
    main()
