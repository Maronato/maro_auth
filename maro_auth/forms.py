from django import forms
from .models import EmailManager
from django.contrib.auth.models import User
from django.forms import ModelForm, Form
from maro_auth import settings
from django.apps import apps
import re

app = apps.get_app_config(settings.PROFILE_APP_NAME)
PROFILE_CLASS = app.get_model(settings.PROFILE_MODEL_NAME)


class LoginForm(Form):
    username = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Senha', required=True, widget=forms.PasswordInput)


class SignupForm(ModelForm):

    first_name = forms.CharField(label='Primeiro nome', max_length=30, required=True)
    email = forms.EmailField(label='Email', required=True)
    last_name = forms.CharField(label='Sobrenome', max_length=30, required=True)

    class Meta:
        model = PROFILE_CLASS
        fields = settings.FIELDS
        exclude = settings.EXCLUDE

    def clean_email(self):
        # Only leave this function here if you want to limit the email formats
        # allowed (e.g. only allow DAC emails)

        # process email
        email = self.cleaned_data['email'].lower()

        # Check if user exists
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError(
                "Usuário já cadastrado!"
            )

        # if limiting users
        if settings.LIMIT_USERS:
            # check email format
            if not re.match(r'^[a-z]\d+@dac.unicamp.br$', email, re.I):
                raise forms.ValidationError(
                    "Email não é da DAC!"
                )
        return email

    def save(self, commit=True):

        # process user creation
        profile = super(SignupForm, self).save(commit=False)

        # set field on current scope
        field = None

        # tries to find a field that points to an User obj
        for f in PROFILE_CLASS._meta.fields:
            try:
                if f.rel.to == User:
                    field = f
                    break
            except:
                pass

        # if the profile has an attribute that points to User, create it
        if field is not None:

            # Create the user obj
            user = User(
                email=self.cleaned_data['email'].lower(),
                username=self.cleaned_data['email'].lower(),
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )

            user.is_active = False
            user.set_unusable_password()

            if commit is True:
                # save user
                user.save()
                # Set profile's user
                setattr(profile, field.name, user)
                # save profile
                profile.save()
                # create emailmanager
                EmailManager.create(user)

        # if it does not, assume it is the user itself
        else:
            user = profile
            user.username = self.cleaned_data['email'].lower()
            user.is_active = False
            user.set_unusable_password()

            if commit is True:
                # save user
                user.save()
                # create emailmanager
                EmailManager.create(user)

        return user
