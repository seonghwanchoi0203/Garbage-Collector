from message.models import Inquiry, Offer
from django import forms
from django.forms import ModelForm


class InquiryAdd(forms.Form):
    garbage_id = forms.CharField(max_length=500, blank=True, null=True)
    title = forms.CharField(max_length=500, blank=True, null=True)
    content = forms.CharField(max_length=500, blank=True, null=True)
    transaction_id = forms.CharField(max_length=255, null=True, blank=True)
    negotiate_price = forms.FloatField(default=0)

class OfferAdd(forms.Form):
    title = forms.CharField(max_length=500, blank=True, null=True)
    content = forms.CharField(max_length=500, blank=True, null=True)
    extended_user_id = forms.CharField(max_length=500, blank=True, null=True)
    inquiry_id = forms.CharField(max_length=500, blank=True, null=True)
    negotiate_price = forms.FloatField(default=0)


class WithdrawForm(forms.Form):
    garbage_id = forms.CharField(max_length=500, blank=True, null=True)
    negotiate_price = forms.FloatField(default=0)


class DeclineForm(forms.Form):
    extended_user_id = forms.CharField(max_length=500, blank=True, null=True)
    inquiry_id = forms.CharField(max_length=500, blank=True, null=True)
    negotiate_price = forms.FloatField(default=0)

