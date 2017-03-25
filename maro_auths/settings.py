from django.conf import settings


def get(key, default):
    getattr(settings, key, default)


# index url name
INDEX_URL_NAME = get('INDEX_URL_NAME', 'index')

# profile url name
PROFILE_URL_NAME = get('PROFILE_URL_NAME', 'profile')

# site url
SITE_URL = get('SITE_URL', 'http://localhost:8000')
