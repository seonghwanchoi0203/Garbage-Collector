from django.db import models

# Create your models here.
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User
import uuid
# from django.contrib.postgres.fields import ArrayField
# from localflavor.us.forms import USPhoneNumberField

class ExtendedUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True, null=True)
    #location = models.CharField(max_length=30, blank=True, null=True)
    #photos = models.ImageField(default='%s/default.png' % settings.MEDIA_URL, upload_to=get_image_path)

    # birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class AdminUser(models.Model):
    registered = models.BooleanField(default=False)
    extended_user = models.OneToOneField(ExtendedUser, primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.extended_user.user.username

    def get_allauth_user(self):
        return self.extended_user.user




@receiver(user_signed_up)
def do_stuff_after_sign_up(sender, **kwargs):
    try:
        # kwargs['sociallogin']
        request = kwargs['request']
        user = kwargs['user']
        new_user = ExtendedUser.objects.create(user=user)
        new_admin_user = AdminUser.objects.create(extended_user=new_user)
        new_admin_user.registered = True;
        new_admin_user.save()
        new_user.save()
        user.save()
    except KeyError:
        try:
            user = kwargs['user']
            new_user = ExtendedUser.objects.create(user=user)
            new_admin_user = AdminUser.objects.create(extended_user=new_user)
            new_admin_user.registered = True;
            new_admin_user.save()
            new_user.save()
            user.save()
        except KeyError:
            pass
