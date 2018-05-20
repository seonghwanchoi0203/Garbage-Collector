from garbage.models import Garbage
from django import forms
from django.forms import ModelForm


class GarbageEdit(ModelForm):
    class Meta:
        model = Garbage
        fields = ['title', 'description', 'cost','zipcode','condition','photos']


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


class GarbageAdd(ModelForm):
    class Meta:
        model = Garbage
        fields = ['title', 'description','cost','zipcode','condition','photos']

    Latitude = forms.FloatField(required=False)
    Longitude = forms.FloatField(required=False)
    #description = forms.CharField(max_length=256)
    #cost = forms.CharField()
    #photos = forms.ImageField()
    #zipcode = forms.CharField()
    #condition = forms.CharField()


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
