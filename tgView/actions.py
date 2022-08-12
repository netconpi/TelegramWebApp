
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import json
import db
import text
import key_markups


# Define a `/start` command handler.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    registred = db.postgree_fetch(f'''SELECT telegram_id FROM "tgWebAppRender_company" WHERE telegram_id=''' + f"'{update.message['chat']['id']}'")
    if not registred:
        await update.message.reply_text(
            text.INVITE_TO_REGISTER,
            reply_markup=InlineKeyboardMarkup(key_markups.add_company_markup),
        )
    else:
        await update.message.reply_text(
            text.START,
            reply_markup=InlineKeyboardMarkup(key_markups.start),
        )

