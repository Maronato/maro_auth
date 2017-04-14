Quick start
-----------
1. Add `maro-auth` to your `requirements.txt`

2. Add `maro_auth` to the _end_ of your INSTALLED_APPS setting like this::
    ```Python
    INSTALLED_APPS = [
        ...
        'maro_auth',
    ]
    ```

3. Include the URLconf in your project urls.py like this::

    `url(r'^auth/', include('maro_auth.urls', namespace='maro_auth')),`

4. Run `python manage.py migrate` to create the auth models.

5. Add the following settings to your `settings.py` to configure the app:

    ```Python
    INDEX_URL_NAME = 'index'  # name of your project's index url. Used on redirects

    PROFILE_URL_NAME = 'profile'  # name of your project's profile url. Used on redirects

    SITE_URL = 'http://localhost:8000'  # your site's url, without the '/' at the end. Used on emails

    PROJECT_NAME = 'Projeto Genérico'  # your project's name. Used on emails

    LIMIT_USERS = True  # Whether or not to limit your users to DAC users only. Used during signup evaluation

    PROFILE_APP_NAME = 'auth'  # (optional) the name of the app containing your Profile model

    PROFILE_MODEL_NAME = 'User'  # (optional) the name of the Profile model you'll want to use and associate with your Users

    FIELDS = ('first_name', 'email', 'last_name')  # (optional) the Profile fields that you want to include in your signup form

    EXCLUDE = ('username', 'password1', 'password2')  # (optional) the Profile fields that you want to exclude from your signup form
    ```

    And also don't forget to setup your email sending protocols:
    ```Python
    DEFAULT_FROM_EMAIL = 'example@example.com'
    EMAIL_HOST_USER = 'example@example.com'
    EMAIL_HOST_PASSWORD = 'super_s3cret'
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    SERVER_EMAIL = 'example@example.com'
    ```

    And, if you want to receive error logs:

    `ADMINS = [('Admin', 'admin@example.com'), ]`

Customizing the templates
-------------------------

Add a folder called `maro_auth` to your app's templates, as in

```
|my_app/
|---- templates/
    |---- maro_auth/
        |---- email/
            |---- change_email.html
            |---- change_email.txt
            |---- reset_password.html
            |---- reset_password.txt
            |---- welcome_email.html
            |---- welcome_email.txt
        |---- login.html
        |---- reset_password.html
        |---- reset_password_complete.html
        |---- reset_password_confirm.html
        |---- reset_password_done.html
        |---- set_password.html
        |---- signup.html
```

You can now modify all the default templates at will

