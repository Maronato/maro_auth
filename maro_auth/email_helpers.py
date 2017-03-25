from django.core.mail import send_mail
from django.template.loader import render_to_string
from .settings import *
from django.urls import reverse


# https://github.com/mailgun/transactional-email-templates
def welcome_email(manager):
    context = {
        'username': manager.user.first_name,
        'url': SITE_URL + reverse('maro_auth:password_set', args={manager.key}),
        'project_url': SITE_URL,
        'project_name': PROJECT_NAME
    }
    to = manager.active_email
    fr = str(DEFAULT_FROM_EMAIL)
    msg_plain = render_to_string('maro_auth/email/welcome_email.txt', context)
    msg_html = render_to_string('maro_auth/email/welcome_email.html', context)

    send_mail(
        'Confirmação de Email',
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def send_change_email(manager, email):
    context = {
        'username': manager.user.first_name,
        'url': SITE_URL + reverse('maro_auth:change_email', args={manager.key}),
        'project_url': SITE_URL,
        'project_name': PROJECT_NAME
    }
    to = email
    fr = str(DEFAULT_FROM_EMAIL)
    msg_plain = render_to_string('maro_auth/email/change_email.txt', context)
    msg_html = render_to_string('maro_auth/email/change_email.html', context)

    send_mail(
        'Alteração de email',
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )
