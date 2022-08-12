
import text
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo, InlineKeyboardButton

add_company = [
    [
        InlineKeyboardButton(
            text.INVITE_TO_REGISTER_BTN, 
            web_app=WebAppInfo(url="https://singup.ru/add_company"),
        ),
    ],
]

# add_company_markup = InlineKeyboardMarkup(add_company)

def generate_start(user_id):
    start = [
        [
            InlineKeyboardButton(
                text.LK_BTN, 
                web_app=WebAppInfo(url=f"https://singup.ru/lk?tg_id={user_id}"),
            ),
        ],
    ]
    return start

# start_markup = InlineKeyboardMarkup(start)
