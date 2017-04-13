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

            # try to confirm the key
            user = EmailManager.confirm(key)
            # if the key was confirmed
            if user.is_active:
                form.save()
                # Login the new user and validate their accounts
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Sua conta foi ativada com sucesso!')
                return redirect(profile)
            # if the key was not confirmed
            else:
                messages.add_message(request, messages.SUCCESS, 'Não foi possível confirmar seu email!')

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


def login_user(request):
    # Custom login method
    context = {}
    if request.method == 'POST':
        # Recover username and password
        username = request.POST['username'].lower()
        password = request.POST['password']
        # Authenticates them
        user = authenticate(username=username, password=password)
        # If the user exists
        if user is not None:
            # and has confirmed their emails
            if user.is_active:
                # Login them and redirect to the dashboard
                login(request, user)
                return redirect(PROFILE_URL_NAME)
            # If the user has not verified their emails, tell them that
            messages.add_message(request, messages.SUCCESS, 'Seu usuário está inativo. Procure pelo email de confirmação em sua caixa de entrada.')
        # If the user does not exist, tell them that
        else:
            messages.add_message(request, messages.SUCCESS, 'Usuário ou senha incorretos.')
        # Reload the username and pass it as the context so that ppl dont have to retype it
        context = {'username': username}
    return render(request, 'maro_auth/login.html', context)
