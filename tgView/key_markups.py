
import text
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup

add_company = [
    [
        InlineKeyboardButton(
            text.INVITE_TO_REGISTER_BTN, 
            web_app=WebAppInfo(url="https://singup.ru/create_account/"),
        ),
    ],
]


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


def add_event(user_id):
    event = [
        [
            InlineKeyboardButton(
                text.EVENT_BTN, 
                web_app=WebAppInfo(url=f"https://singup.ru/creat_ev?tg_id={user_id}"),
            ),
        ],
    ]
    return event


def events(user_id):
    event = [
        [
            InlineKeyboardButton(
                text.EVENTS_BTN, 
                web_app=WebAppInfo(url=f"https://singup.ru/calendar-task-list/?tg_id={user_id}"),
            ),
        ],
    ]
    return event


def agree_executor():
    reply_keyboard = [
        [text.EXEC_AGREE],
        [text.EXEC_CANCEL],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    return markup
# start_markup = InlineKeyboardMarkup(start)
