from django import forms
from django.forms import ModelForm
from .models import CheckoutInformation

from django.core.exceptions import ValidationError

class CheckoutForm(ModelForm):
    firstName = forms.TextInput()
    lastName = forms.TextInput()
    email = forms.EmailField()
    phoneNumber = forms.TextInput()

    class Meta:
        model = CheckoutInformation
        fields = ['firstName', 'lastName', 'email', 'phoneNumber']

    def clean_firstName(self):
        data = self.cleaned_data['firstName']

        return data
