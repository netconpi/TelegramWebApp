
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


start = [
    [
        InlineKeyboardButton(
            text.LK_BTN, 
            # callback_data="Btn", 
            web_app=WebAppInfo(url="https://singup.ru/lk"),
        ),
    ],
]

# start_markup = InlineKeyboardMarkup(start)
