# forms.py

from django import forms

class PasswordResetRequestForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email')
