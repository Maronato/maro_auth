from .models import EmailManager
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import login
from .settings import *
from .forms import SignupForm
# Create your views here.

# index url
index = INDEX_URL_NAME

# profile url
profile = PROFILE_URL_NAME


def signup(request):
    """Signup
    generates signup form and processess it
    """

    # if submitting a new account
    if request.method == 'POST':
        # collect post data
        form = SignupForm(request.POST)
        # if form is valid
        if form.is_valid():
            # save it and redirect to index
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Email de confirmação enviado!')
            return redirect(index)
    # if get, create a form
    else:
        form = SignupForm()
    # render signup page and return it
    return render(request, 'maro_auth/signup.html', {'form': form})


def confirm_email(request, key):
    """Confirm Email
    receives a key and tries to confirm it
    if the key is valid, reload the page with a form to set their passwords
    when the user submits the password, set it as key's owner password, confirm the key and login the user
    """

    # Get the key's owner
    manager = EmailManager.find_key(key)

    # If the key does not exist or was already used, redirect to index and tell them that
    if not manager or manager.is_active:
        messages.add_message(request, messages.SUCCESS, 'Chave de ativação inválida ou já usada.')
        return redirect(index)

    # If the user is submitting their new passwords(POST)
    if request.method == 'POST':
        # Load the data
        form = SetPasswordForm(manager.user, request.POST)
        # If the password is valid
        if form.is_valid():
            form.save()
            # Login the new user and validate their accounts
            login(request, manager.user)
            EmailManager.confirm(key)
            messages.add_message(request, messages.SUCCESS, 'Sua conta foi ativada com sucesso!')
            return redirect(profile)

    # If the user just clicked the activation link, generate a password form
    else:
        form = SetPasswordForm(manager.user)
    return render(request, 'maro_auth/set_password.html', {'form': form, 'key': key})


def change_email(request, key):
    """Change Email
    receives a key and changes their email
    """

    # Get the key's owner
    manager = EmailManager.find_key(key)
    # If the key does not exist or was already used, redirect to index and tell them that
    if not manager:
        messages.add_message(request, messages.SUCCESS, 'Chave inválida.')

    else:
        # Confirm the key
        EmailManager.confirm(key)
        messages.add_message(request, messages.SUCCESS, 'Pronto! Email alterado!')

    return redirect(index)
