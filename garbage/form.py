from garbage.models import Garbage
from django import forms
from django.forms import ModelForm


class GarbageEdit(ModelForm):
    class Meta:
        model = Garbage
        #fields = ('title', 'zipcode', 'cost', 'condition', 'description')
        exclude = ['buyer', 'owner', 'location', 'soldDate', 'watched']


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


class GarbageAdd(ModelForm):
    class Meta:
        model = Garbage
        #fields = ('title', 'zipcode', 'cost', 'condition', 'description')
        exclude = ['buyer', 'owner', 'location', 'soldDate', 'watched']


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
