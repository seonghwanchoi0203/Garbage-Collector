from garbage.models import Garbage
from django import forms


class GarbageEdit(forms.ModelForm):
    class Meta:
        model = Garbage
        exclude = ['buyer', 'owner', 'location', 'soldDate', 'watched']


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


class GarbageAdd(forms.ModelForm):
    class Meta:
        model = Garbage
        exclude = ['buyer', 'owner', 'location', 'soldDate', 'watched']


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
