
import datetime as dt_lib

def convert_strlist2list(strlist: str) -> list:
    working_days = []

    for i in strlist:
        if i >= '0' and i <= '9':
            working_days.append(int(i))

    return working_days


dates_name = {
    'Monday': 'Понедельник',
    'Tuesday': 'Вторник',
    'Wednesday': 'Среда',
    'Thursday': 'Четверг',
    'Friday': 'Пятница',
    'Saturday': 'Суббота',
    'Sunday': 'Воскресенье',
}

def is_working_weekday(date: dt_lib.datetime, weekday: list) -> bool:
    weekday_dateobj = date.weekday() + 1
    for day in weekday:
        if int(day) == weekday_dateobj:
            return True
        else:
            return False 
