from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User
#from django.contrib.postgres.fields import ArrayField
#from localflavor.us.forms import USPhoneNumberField
class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    #birth_date = models.DateField(null=True, blank=True)
    def __str__(self):
    	return self.main_user.username

@receiver(user_signed_up)
def do_stuff_after_sign_up(sender, **kwargs):
  try:
    #kwargs['sociallogin']
    request = kwargs['request']
    user = kwargs['user']
    new_user = ExtendedUser.objects.create(main_user=user)
    new_user.save()
    user.save()
  except KeyError:
    try:
      user = kwargs['user']
      new_user = ExtendedUser.objects.create(main_user=user)
      new_user.save()
      user.save()
    except KeyError:
      pass 