from datetime import datetime
from User_backend.user import get_time_format
from constants import *

def get_datetime_object(user, input_str):
    if input_str == None or input_str == '':
        return None
    elif input_str.lower() in FUZZY_DATES:
        return fuzzy_str_to_datetime(input_str)
    elif get_time_format(user) == TIME_FORMAT_24_HR:
        return datetime.strptime(input_str, CONVERT_24_HR)
    return datetime.strptime(input_str, CONVERT_12_HR)

def fuzzy_str_to_datetime(input_str):
    if input_str.lower() == 'now':
        return datetime.strptime(FUZZY_NOW_STR, CONVERT_24_HR)
    elif input_str.lower() == 'soon':
        return datetime.strptime(FUZZY_SOON_STR, CONVERT_24_HR)
    elif input_str.lower() == 'someday':
        return datetime.strptime(FUZZY_SOMEDAY_STR, CONVERT_24_HR)
    
def get_datetime_str(user, input_datetime):
    if input_datetime == None:
        return ''
    elif input_datetime.year == FUZZY_YEAR:
        return fuzzy_datetime_to_str(input_datetime)
    elif get_time_format(user) == TIME_FORMAT_24_HR:
        return datetime.strftime(CONVERT_24_HR)
    return datetime.strftime(CONVERT_12_HR)

def fuzzy_datetime_to_str(input_datetime):
    if input_datetime.day == FUZZY_NOW_DAY:
        return 'now'
    elif input_datetime.day == FUZZY_SOON_DAY:
        return 'soon'
    elif input_datetime.day == FUZZY_SOMEDAY_DAY:
        return 'someday'
