from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.models import EmailAddress

# extend django built-in User
class User(AbstractUser, models.Model):
    
    avatar = models.ImageField(upload_to="avatar", default="avatar/default.png", verbose_name="avatar", blank=True, null=True)

    def email_verified(self):
        if self.is_authenticated:
            result = EmailAddress.objects.filter(email=self.email)
            if len(result):
                return result[0].verified
            else:
                return False

    class Meta:
        # define table name and its plural form in Admin
        verbose_name = "userinfo" 
        verbose_name_plural = verbose_name
        # define the default order shown in admin
        ordering = ["-id"]
    
    # what to show in admin when refer to this table
    def __str__(self):
        return self.username
