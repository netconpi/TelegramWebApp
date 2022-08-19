
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import json
import db
import text
import key_markups

# Not using, for ConversationHandler
# BECOME_EXECUTOR STATES
AGREE = range(1)

# Define a `/start` command handler.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    registred = db.postgree_fetch(f'''SELECT telegram_id FROM "tgWebAppRender_userapp" WHERE telegram_id=''' + f"'{update.message['chat']['id']}'")
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


#Define executior be process
async def executor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print(update)
    await update.message.reply_text(
        text.EXEC_INTRO,
        reply_markup=InlineKeyboardMarkup(key_markups.become_executor),
    )


# continue executior confirm 
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


# Add event def 
async def addevent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if db.check_company(update.message['chat']['id']):
        await update.message.reply_text(
            text.EVENT, 
            reply_markup=InlineKeyboardMarkup(key_markups.add_event(update.message['chat']['id'])),
        )
    else:
        await update.message.reply_text(
            text.NOT_EXECUTOR, 
        )

    # return ConversationHandler.END


# Edit event page (Calendar + View + Edit)
async def events(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if db.check_company(update.message['chat']['id']):
        await update.message.reply_text(
            text.EVENTS, 
            reply_markup=InlineKeyboardMarkup(key_markups.events(update.message['chat']['id'])),
        )
    else:
        await update.message.reply_text(
            text.NOT_EXECUTOR, 
        )


# Not using, for ConversationHandler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        text.CANCEL, reply_markup=key_markups.ReplyKeyboardRemove()
    )
    return ConversationHandler.END
    

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass

