from django.conf import settings


def get(key, default):
    getattr(settings, key, default)


# index url name
INDEX_URL_NAME = get('INDEX_URL_NAME', 'index')

# profile url name
PROFILE_URL_NAME = get('PROFILE_URL_NAME', 'profile')

# site url
SITE_URL = get('SITE_URL', 'http://localhost:8000')

# project name
PROJECT_NAME = get('PROJECT_NAME', 'Projeto Genérico')

# whether or not to limit users to only unicamp students
LIMIT_USERS = get('LIMIT_USERS', True)

# Email sending settings
DEFAULT_FROM_EMAIL = get('DEFAULT_FROM_EMAIL', 'example@example.com')
EMAIL_HOST_USER = get('EMAIL_HOST_USER', 'example@example.com')
EMAIL_HOST_PASSWORD = get('EMAIL_HOST_PASSWORD', 'super_s3cret')
EMAIL_USE_TLS = get('EMAIL_USE_TLS', True)
EMAIL_HOST = get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = get('EMAIL_PORT', 587)
SERVER_EMAIL = get('SERVER_EMAIL', 'example@example.com')

# List of admins to receive emails when something bad happens
ADMINS = get('ADMINS', [('Admin', 'example@example.com'), ])
