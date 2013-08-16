
# The regex used to extract tags from a text
TAG_REGEX = ur'(?:^|[\s])(@[\w\/\.\-\:]*\w)'

# The regex used to validate email
EMAIL_REGEX = ur'[\.\w]{1,}[@]\w+[.]\w+'

# The regexes used for start date and due date
START_STRING_REGEX = ur'(start\s*:\s*\d{1,2}\/\d{1,2}\/\d{2,4})'
DUE_STRING_REGEX = ur'(due\s*:\s*\d{1,2}\/\d{1,2}\/\d{2,4})'
DATE_REGEX = ur'\d{1,2}\/\d{1,2}\/\d{2,4}'

# Task status
IS_ACTIVE = 0
IS_DONE = 1
IS_DISMISSED = 2

# Folder status dictionary
FOLDER_STATUS_STR = {
    -1: 'All',
    IS_ACTIVE: 'Active',
    IS_DONE: 'Done',
    IS_DISMISSED: 'Dismissed',
}

FOLDER_STATUS_INT = {
    'All': -1,
    'Active': IS_ACTIVE,
    'Done': IS_DONE,
    'Dismissed': IS_DISMISSED,
}

# Task sharing folders
YOUR_SHARED = -2
THEY_SHARED = -3

# Task date
IS_START_DATE = 0
IS_DUE_DATE = 1

# User preference time format
TIME_FORMAT_24_HR = 0
TIME_FORMAT_12_HR = 1

# Conversion strings for both the time formats
CONVERT_24_HR = '%d/%m/%y'
CONVERT_12_HR = '%d/%m/%y'

CONVERT_24_HR_FULL_YEAR = '%d/%m/%Y'
CONVERT_12_HR_FULL_YEAR = '%d/%m/%Y'

CONVERT_24_HR_WITH_TIME = '%d/%m/%y %H:%M:%S'
CONVERT_12_HR_WITH_TIME = '%d/%m/%y %I:%M %p'

# Fuzzy date list
FUZZY_DATES = ['now', 'soon', 'someday']

# Don't use the below constants anywhere in the project right now.
# Fuzzy Dates aren't confirmed yet.
##############################################################################
# Fuzzy date strings
#FUZZY_NOW_STR = '01/01/2152 00:00'
#FUZZY_SOON_STR = '02/01/2152 00:00'
#FUZZY_SOMEDAY_STR = '03/01/2152 00:00'
#FUZZY_YEAR = '2152'
#FUZZY_NOW_DAY = 1
#FUZZY_SOON_DAY = 2
#FUZZY_SOMEDAY_DAY = 3
##############################################################################

# User related
USER_LOGGED_IN = 0
USER_ACCOUNT_DISABLED = 1
USER_INVALID = 2

# Groups related
NON_GROUPED = 0
GROUPED = 1

# Gravatar profile URL
GRAVATAR_BASE_URL = "http://www.gravatar.com/"

# Logs
LOG_NEW_TASK = 0
LOG_TASK_MODIFY = 1
LOG_TASK_SHARE = 2
LOG_TASK_STATUS = 3
LOG_TASK_DELETE = 4
