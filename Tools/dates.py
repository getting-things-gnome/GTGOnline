from datetime import datetime, timedelta
from User_backend.user import get_time_format
from constants import *

def get_datetime_object(input_str):
    #elif input_str.lower() in FUZZY_DATES:
    #    return fuzzy_str_to_datetime(input_str)
    #elif input_str[-2:].lower() == 'am' or input_str[-2:].lower() == 'pm':
        #return datetime.strptime(input_str, CONVERT_12_HR)
    try:
        if '/' in input_str[-4:]:
            return datetime.strptime(input_str, CONVERT_24_HR)
        else:
            return datetime.strptime(input_str, CONVERT_24_HR_FULL_YEAR)
    except Exception:
        return None


# Don't use the below 2 functions anywhere in the project right now.
# Fuzzy Dates aren't confirmed yet.
###############################################################################
#def fuzzy_str_to_datetime(input_str):
#    if input_str.lower() == 'now':
#        return datetime.strptime(FUZZY_NOW_STR, CONVERT_24_HR)
#    elif input_str.lower() == 'soon':
#        return datetime.strptime(FUZZY_SOON_STR, CONVERT_24_HR)
#    elif input_str.lower() == 'someday':
#        return datetime.strptime(FUZZY_SOMEDAY_STR, CONVERT_24_HR)   
#
#def fuzzy_datetime_to_str(input_datetime):
#    if input_datetime.day == FUZZY_NOW_DAY:
#        return 'now'
#    elif input_datetime.day == FUZZY_SOON_DAY:
#        return 'soon'
#    elif input_datetime.day == FUZZY_SOMEDAY_DAY:
#        return 'someday'
############################################################################### 

def get_datetime_str(user, input_datetime):
    if input_datetime == None or not isinstance(input_datetime, datetime):
        return ''
    #elif input_datetime.year == FUZZY_YEAR:
    #    return fuzzy_datetime_to_str(input_datetime)
    elif get_time_format(user) == TIME_FORMAT_24_HR:
        return input_datetime.strftime(CONVERT_24_HR)
    return input_datetime.strftime(CONVERT_12_HR)
    
def get_days_left(input_datetime):
    if input_datetime == None:
        return 99999
    return (input_datetime - datetime.now()).days

def get_current_datetime_object():
    return datetime.now()

def compare_dates(date1, date2):
    if date1 == None:
        return (0, None)
    elif date2 == None:
        return (0, None)
    else:
        if date1 < date2:
            return (1, 0)
        elif date1 > date2:
            return (1, 1)
        else:
            return (1, None)

def get_datetime_from_days_left(days_left):
    that_date = datetime.now() + timedelta(days = days_left)
    return datetime(that_date.year, that_date.month, that_date.day)
