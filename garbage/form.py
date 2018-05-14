from garbage.models import Garbage
from django import forms
from django.forms import ModelForm


class GarbageEdit(ModelForm):
    class Meta:
        model = Garbage
        fields = ['title', 'description', 'cost','zipcode','condition']


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


class GarbageAdd(forms.Form):

    title = forms.CharField(max_length=30)
    description = forms.CharField(max_length=256)
    cost = forms.CharField()
    # photos = forms.ImageField(default='%s/default.png' % settings.MEDIA_URL, upload_to=get_image_path)
    zipcode = forms.CharField()
    condition = forms.CharField()


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
