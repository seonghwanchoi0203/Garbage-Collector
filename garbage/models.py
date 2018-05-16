from django.db import models
import json
from userprof.models import AdminUser, ExtendedUser
from django.conf import settings
from jsonfield import JSONField
import os
import datetime
import uuid

# Create your models here.
#


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class Garbage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    title = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=256)
    cost = models.IntegerField(blank=True, null=True, default=0)
    photos = models.ImageField(default='%sdefault.png' % settings.MEDIA_URL, upload_to=get_image_path)
    zipcode = models.IntegerField(blank=True, null=True)
    condition = models.IntegerField(blank=True, null=True, default=5)

    distance = None
    # location = models.PointField(null=True, blank=True)

    owner = models.ForeignKey(AdminUser, on_delete=models.CASCADE, related_name='owner')
    buyer = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, related_name='buyer', blank=True, null=True)

    postdate = models.DateField(auto_now_add=True)
    soldDate = models.DateField(blank=True, null=True)

    sold = models.BooleanField(default=False)
    watched = models.ManyToManyField(ExtendedUser, blank=True, null=True, through='Watch')


    def reserve(self, user, date):
        if self.sold:
            return 0
        else:
            self.buyer = user
            self.soldDate = datetime.date.today()
            self.sold = False
        return 1

    # def save(self, *args, **kwargs):
    # only update location if null. Edit garbage page can handle updating location.
    # if not self.location:
    # g = GoogleV3()
    # p = g.geocode("{}, {}, {} {}".format(self.street_address, self.city, self.state, self.zipcode))
    # self.location = Point(p.longitude, p.latitude)

    # hopefully solves the issue of django default string
    #   if isinstance(self.amenities, str):
    #       self.amenities = json.loads(self.amenities)
    #   if isinstance(self.parking_spot_avail, str):
    #       self.parking_spot_avail = json.loads(self.parking_spot_avail)
    #   super(Garbage, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Watch(models.Model):
    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    garbage = models.ForeignKey(Garbage, on_delete=models.CASCADE)
    date_watch = models.DateField()

    def __str__(self):
        return "%s" % self.user

