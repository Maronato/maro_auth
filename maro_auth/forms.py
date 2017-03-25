from django import forms
from .models import EmailManager
from django.contrib.auth.models import User
from django.forms import ModelForm
import re


class SignupForm(ModelForm):

    first_name = forms.CharField(label='Primeiro nome', max_length=30, required=True)
    email = forms.EmailField(label='Seu email da DAC', required=True)
    last_name = forms.CharField(label='Sobrenome', max_length=30, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'email', 'last_name')
        exclude = ('username', 'password1', 'password2')

    def clean_email(self):
        # Only leave this function here if you want to limit the email formats
        # allowed (e.g. only allow DAC emails)

        # process email
        email = self.cleaned_data['email']

        # check email format
        if not re.match(r'^[a-z]\d+@dac.unicamp.br$', email, re.I):
            raise forms.ValidationError(
                "Email não é da DAC!"
            )
        return email.lower()

    def save(self, commit=True):
        # process user creation
        user = super(SignupForm, self).save(commit=False)

        # set user variables
        user.email = self.cleaned_data['email']

        # WARNING: username is being set as the email.
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = False
        user.set_unusable_password()

        # if commit is true, save user and create emailmanager
        if commit is True:
            user.save()
            EmailManager.create(user)

        return user
