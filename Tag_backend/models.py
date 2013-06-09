from django.db import models
from django.conf import settings

# Create your models here.

class Tag(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length = 250)
    color = models.CharField(max_length = 10)
    icon = models.CharField(max_length = 50)
    
    class Meta:
        unique_together = ("user", "name")
    
    
    def __unicode__(self, ):
        return self.name
