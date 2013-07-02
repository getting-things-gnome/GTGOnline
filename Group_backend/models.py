from django.db import models
from django.conf import settings

# Create your models here.

class Group(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, \
                             related_name = "group_set")
    name = models.CharField(max_length = 250)
    color = models.CharField(max_length = 10)
    icon = models.CharField(max_length = 50)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, \
                                     related_name = "member_set")
    
    class Meta:
        unique_together = ("user", "name")
    
    def __unicode__(self, ):
        return self.name
