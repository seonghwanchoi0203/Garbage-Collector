from message.models import Inquiry, Offer
from django import forms
from django.forms import ModelForm


class InquiryAdd(ModelForm):
    class Meta:
        model = Inquiry


class OfferAdd(ModelForm):
    class Meta:
        model = Offer

