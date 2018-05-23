from message.models import Inquiry, Offer
from django import forms
from django.forms import ModelForm


class InquiryAdd(forms.Form):
    garbage_id = forms.CharField()
    title = forms.CharField()
    content = forms.CharField()
    transaction_id = forms.CharField()
    negotiate_price = forms.FloatField()

class OfferAdd(forms.Form):
    title = forms.CharField()
    content = forms.CharField()
    extended_user_id = forms.CharField()
    inquiry_id = forms.CharField()
    negotiate_price = forms.FloatField()


class WithdrawForm(forms.Form):
    garbage_id = forms.CharField()
    negotiate_price = forms.FloatField()


class DeclineForm(forms.Form):
    extended_user_id = forms.CharField()
    inquiry_id = forms.CharField()
    negotiate_price = forms.FloatField()

