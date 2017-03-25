Quick start
-----------
1. Add `git+https://github.com/Maronato/maro_auth.git` to your `requirements.txt`

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

5. Add the following settings to your `settings.py`:

    ```Python
    INDEX_URL_NAME = 'index'  # name of your project's index url

    PROFILE_URL_NAME = 'profile'  # name of your project's profile url

    SITE_URL = 'http://localhost:8000'  # your site's url, without the '/' at the end

    PROJECT_NAME = 'Projeto Genérico'  # your project's name

    LIMIT_USERS = True  # Whether or not to limit your users to DAC users only
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

