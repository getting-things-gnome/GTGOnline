from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class User_preferences(models.Model):
    TIME_FORMAT = (
        (0, '24-Hour'),
        (1, '12-Hour'),
    )
    user = models.ForeignKey(get_user_model())
    time_format = models.SmallIntegerField(choices = TIME_FORMAT, default = 0)
