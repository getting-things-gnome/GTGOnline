
# The regex used to extract tags from a text
TAG_REGEX = '(?:^|[\s])(@[\w\/\.\-\:]*\w)'

# Task status
IS_ACTIVE = 0
IS_DONE = 1
IS_DISMISSED = 2

# User preference time format
TIME_FORMAT_24_HR = 0
TIME_FORMAT_12_HR = 1

# Conversion strings for both the time formats
CONVERT_24_HR = '%d/%m/%Y %H:%M'
CONVERT_12_HR = '%d/%m/%Y %I:%M %p'

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
