from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Tag(models.Model):
    user = models.ForeignKey(get_user_model())
    name = models.CharField(max_length = 300)
    color = models.CharField(max_length = 10)
    icon = models.CharField(max_length = 50)
    
    class Meta:
        unique_together = ("user", "name")
    
    
    def __unicode__(self, ):
        return self.name
