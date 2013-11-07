from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class User_preferences(models.Model):
    TIME_FORMAT = (
        (0, '24-Hour'),
        (1, '12-Hour'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    time_format = models.SmallIntegerField(choices = TIME_FORMAT, default = 0)

class MyUserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an email address')
 
        user = self.model(
            email=MyUserManager.normalize_email(email),
        )
 
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    #username = models.CharField(max_length = 5, db_index = True)
    email = models.CharField(max_length = 254, unique = True, db_index = True)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 50)
    #api_key = models.CharField(max_length = 50, unique = True)
    
    USERNAME_FIELD = 'email'
    objects = MyUserManager()
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    def get_full_name(self):
        # For this case we return email. Could also be User.first_name User.last_name if you have these fields
        return self.first_name + " " + self.last_name
 
    def get_short_name(self):
        # For this case we return email. Could also be User.first_name if you have this field
        return self.first_name
 
    #def get_api_key(self):
        #return self.api_key

    def __unicode__(self):
        return self.email
 
    def has_perm(self, perm, obj=None):
        # Handle whether the user has a specific permission?"
        return True
 
    def has_module_perms(self, app_label):
        # Handle whether the user has permissions to view the app `app_label`?"
        return True
 
    @property
    def is_staff(self):
        # Handle whether the user is a member of staff?"
        return self.is_admin
