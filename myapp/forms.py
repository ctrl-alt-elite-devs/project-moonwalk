from django import forms

from django.core.exceptions import ValidationError



class CheckoutForm(forms.Form):
    firstName = forms.CharField()
    lastName = forms.CharField()
    email = forms.EmailField()
    phoneNumber = forms.CharField()

    def clean_firstName(self):
        data = self.cleaned_data['firstName']

        return data
