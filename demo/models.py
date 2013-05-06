from django.db import models

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    tags = models.CharField(max_length=200)
    done = models.IntegerField(default = 0)
    dismissed = models.IntegerField(default = 0)
    subtasks = models.CharField(max_length = 200)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=10)
    icon = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
