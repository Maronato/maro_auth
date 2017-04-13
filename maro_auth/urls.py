from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .settings import *
import maro_auth.views as views
from django.core.urlresolvers import reverse_lazy

# index url
index = INDEX_URL_NAME

# profile url
profile = PROFILE_URL_NAME

urlpatterns = [

    # Signup form
    url(r'^signup/', views.signup, name='signup'),

    # login
    url(r'^login/', views.login_user, name='login'),

    # logout
    url(r'^logout/$', auth_views.logout, {'next_page': reverse_lazy(index)}, name='logout'),

    # Receives a key and verifies the user if the key is valid. Also asks the user to create a password
    url(r'^confirm-email/(?P<key>[\w]+)', views.confirm_email, name='password_set'),

    # Receives a key and verifies the user if the key is valid. If is, changes their active email
    url(r'^change-email/(?P<key>[\w]+)', views.change_email, name='change_email'),

    # Django's built-in password reset method
    url(r'^reset-password/$', password_reset, {'email_template_name': 'maro_auth/email/reset_password.html', 'html_email_template_name': 'maro_auth/email/reset_password.html', 'template_name': 'maro_auth/reset_password.html', 'post_reset_redirect': reverse_lazy('maro_auth:password_reset_done')}, name='password_reset'),
    url(r'^reset-password-done/$', password_reset_done, {'template_name': 'maro_auth/reset_password_done.html'}, name='password_reset_done'),
    url(r'^reset-password-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {'template_name': 'maro_auth/reset_password_confirm.html', 'post_reset_redirect': reverse_lazy('maro_auth:password_reset_complete')}, name='password_reset_confirm'),
    url(r'^reset-password-complete/$', password_reset_complete, {'template_name': 'maro_auth/reset_password_complete.html'}, name='password_reset_complete'),
]
