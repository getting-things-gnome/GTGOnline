from django.db import models
from django.conf import settings
from Tag_backend.models import Tag

# Create your models here.

class Task(models.Model):
    TASK_STATUS = (
        (0, 'Active'),
        (1, 'Done'),
        (2, 'Dismissed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length = 250, null = False, blank = False)
    description = models.TextField()
    start_date = models.DateTimeField(null = True, blank = True)
    due_date = models.DateTimeField(null = True, blank = True)
    closed_date = models.DateTimeField(null = True, blank = True)
    last_modified_date = models.DateTimeField(auto_now = True)
    status = models.SmallIntegerField(choices = TASK_STATUS, default = 0)
    tags = models.ManyToManyField(Tag)
    subtasks = models.ManyToManyField('self', symmetrical = False)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, \
                                         related_name = "shared_set")
    
    class Meta:
        ordering = ['due_date']
    
    def __unicode__(self, ):
        return self.name


class Log(models.Model):
    task = models.ForeignKey(Task)
    log = models.TextField()
