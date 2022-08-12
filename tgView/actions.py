
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import json
import db
import text
import key_markups


# Define a `/start` command handler.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    registred = db.postgree_fetch(f'''SELECT telegram_id FROM "tgWebAppRender_company" WHERE telegram_id=''' + f"'{update.message['chat']['id']}'")
    print(update.message)
    print(registred)
    if not registred:
        keyboard = [
            [
                InlineKeyboardButton(
                    "Пройти регистрацию", 
                    # callback_data="Btn", 
                    web_app=WebAppInfo(url="https://singup.ru/add_company"),
                ),
            ],
        ]

        markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Рады видеть Вас в нашем боте! Это стартовая команда. Мы не нашли учетную запись. Зарегестрируйтесь нажатием на кнопку ЛК",
            reply_markup=markup,
        )
    else:
        await update.message.reply_text(
            "Рады видеть Вас в нашем боте! Это стартовая команда.",
            reply_markup=ReplyKeyboardMarkup.from_button(
                KeyboardButton(
                    text="Личный кабинет",
                    web_app=WebAppInfo(url="https://singup.ru/lk"),
                )
            ),
        )


# Handle incoming WebAppData
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("DATA FROM WEB ARRIVED")
    data = update.effective_message.web_app_data.data
    print(data)
    print(update.effective_message)
    if data == 'registred user':
        await update.message.reply_html(
            text=f"Поздравляю! Аккаунт был успешно создан",
            reply_markup=ReplyKeyboardRemove(),
        )
        db.commit(f"INSERT INTO registred_user (telegram_id, registred) VAlUES ({update.effective_message['chat']['id']}, 1)")


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update)
    # print(update.effective_message)
    # if data == 'registred user':
    #     await update.message.reply_html(
    #         text=f"Поздравляю! Аккаунт был успешно создан",
    #         reply_markup=ReplyKeyboardRemove(),
    #     )
    #     db.commit(f"INSERT INTO registred_user (telegram_id, registred) VAlUES ({update.effective_message['chat']['id']}, 1)")

