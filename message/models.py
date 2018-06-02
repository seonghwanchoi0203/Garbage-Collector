from django.db import models
from userprof.models import ExtendedUser,AdminUser
from garbage.models import Garbage
import uuid
from django.contrib.auth.models import User
#from review.models import Review

# Create your models here.


class Inquiry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, related_name='ExtendedUser_inquiry')
    receiver = models.ForeignKey(AdminUser, on_delete=models.CASCADE, related_name='AdminUser_inquiry')
    garbage = models.ForeignKey(Garbage, on_delete=models.CASCADE, related_name='garbage')
    title = models.CharField(max_length=80, blank=True)
    content = models.CharField(max_length=1000, blank=True)
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    accept = models.BooleanField(default=False)
    withdraw = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    negotiate_price = models.FloatField(default=0)

    def get_garbage(self):
        return self.garbage

    def __str__(self):
        return "%s" % self.sender



class Offer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inquiry = models.ForeignKey(Inquiry,on_delete=models.CASCADE,related_name='inquiry')
    receiver = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, related_name='ExtendedUser_offer')
    sender = models.ForeignKey(AdminUser, on_delete=models.CASCADE, related_name='AdminUser_offer')
    garbage = models.ForeignKey(Garbage,on_delete=models.CASCADE)
    res_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    #is_approved = models.BooleanField(default=False)
    #has_responded = models.BooleanField(default=False)
    #reviewed = models.ForeignKey(Review, null=True, blank=True)
    title = models.CharField(max_length=80, blank=True)
    content = models.CharField(max_length=1000, blank=True)
    negotiate_price = models.FloatField(default=0)
    continueMessage = models.BooleanField(blank=True,default=True)
    decline = models.BooleanField(blank=True,default=False)
    read = models.BooleanField(default=False)

    def __str__(self):
        return "%s -> %s" % (self.inquiry.sender, self.inquiry.receiver)
