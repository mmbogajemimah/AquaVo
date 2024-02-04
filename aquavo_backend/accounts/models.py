from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=40, unique=False, default='')
    email = models.EmailField(_("email address"), unique=True)
    is_shop_owner  = models.BooleanField(default=False)
    phone_no = models.CharField(max_length = 20,blank=True)
    twofa_status = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return "{}".format(self.email)
