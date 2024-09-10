from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Patient

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Patient
        fields = ('username', 'email', 'password1', 'password2','first_name','last_name','genre','date_naissance')

    # Additional customization, like setting attributes, can be done here
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_naissance'].widget.attrs.update({'class':'form-control'})
        self.fields['genre'].widget.attrs.update({'class':'form-control'})