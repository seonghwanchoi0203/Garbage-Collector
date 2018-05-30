from userprof.models import ExtendedUser
from django import forms


class BioForm(forms.ModelForm):
    #bioform_text = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}) )

    class Meta:
        model = ExtendedUser
        #fields = ['bio']
        exclude = ['user','first']

        '''
            # the new bit we're adding
        def __init__(self, *args, **kwargs):
            super(ContactForm, self).__init__(*args, **kwargs)
            self.fields['user'] = ExtendedUser
            self.fields['contact_email'].label = "Your email:"
            self.fields['content'].label =
                "What do you want to say?"
                '''


class ScoreAdd(forms.Form):
        rate = forms.CharField(max_length=30)
