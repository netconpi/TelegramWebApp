
import text
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup

add_company = [
    [
        InlineKeyboardButton(
            text.INVITE_TO_REGISTER_BTN, 
            web_app=WebAppInfo(url="https://singup.ru/add_company"),
        ),
    ],
]

add_company_markup = InlineKeyboardMarkup(add_company)

def generate_start(user_id):
    start = [
        [
            InlineKeyboardButton(
                text.LK_BTN, 
                web_app=WebAppInfo(url=f"https://singup.ru/lk?tg_id={user_id}"),
            ),
            InlineKeyboardButton(
                text.NOTIFICATION_BTN, 
                web_app=WebAppInfo(url=f"https://singup.ru/notifications?tg_id={user_id}"),
            ),
        ],
    ]
    return start


def agree_executor():
    reply_keyboard = [
        [text.EXEC_AGREE],
        [text.EXEC_CANCEL],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    return markup
# start_markup = InlineKeyboardMarkup(start)
