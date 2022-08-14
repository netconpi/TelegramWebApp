
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import json
import db
import text
import key_markups

# BECOME_EXECUTOR STATES
AGREE = range(1)


# Define a `/start` command handler.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    registred = db.postgree_fetch(f'''SELECT telegram_id FROM "tgWebAppRender_company" WHERE telegram_id=''' + f"'{update.message['chat']['id']}'")
    if not registred:
        await update.message.reply_text(
            text.INVITE_TO_REGISTER,
            reply_markup=InlineKeyboardMarkup(key_markups.add_company),
        )
    else:
        await update.message.reply_text(
            text.START,
            reply_markup=InlineKeyboardMarkup(key_markups.generate_start(update.message['chat']['id'])),
        )


async def executor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print(update)
    await update.message.reply_text(
        text.EXEC_INTRO,
        reply_markup=key_markups.agree_executor(),
    )

    return AGREE


async def exec_state(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    print(update.message.text)

    if update.message.text == text.EXEC_AGREE: 

        db.postgree_commit(f'''UPDATE "tgWebAppRender_company" SET company_type='executor' WHERE telegram_id=''' + f"'{update.message['chat']['id']}'")

        await update.message.reply_text(
            text.EXEC_BECOME,
            reply_markup=key_markups.ReplyKeyboardRemove(),
        )
    else: 
        await update.message.reply_text(
            text.EXEC_NOPE,
            reply_markup=key_markups.ReplyKeyboardRemove(),
        )
    
    return ConversationHandler.END


async def addevent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text.EVENT, 
        reply_markup=InlineKeyboardMarkup(key_markups.add_event(update.message['chat']['id'])),
    )

    # return ConversationHandler.END


async def pending(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text.EVENT, 
        reply_markup=InlineKeyboardMarkup(key_markups.add_event(update.message['chat']['id'])),
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        text.CANCEL, reply_markup=key_markups.ReplyKeyboardRemove()
    )
    return ConversationHandler.END
    

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass

