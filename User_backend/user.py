from django.contrib.auth.models import User
from User_backend.models import User_preferences

def get_user_object(user):
    if isinstance(user, str) or isinstance(user, unicode):
        return User.objects.get(username = user)
    elif isinstance(user, User):
        return user
    
def get_first_name(user):
    user = get_user_object(user)
    return user.get_short_name()

def get_time_format(user):
    return User_preferences.objects.get(user = user).time_format



