Quick start
-----------
1. Add `git+https://github.com/Maronato/maro_auth.git` to your `requirements.txt`

2. Add `maro_auth` to the _end_ of your INSTALLED_APPS setting like this::
    ```
    INSTALLED_APPS = [
        ...
        'maro_auth',
    ]
    ```

3. Include the URLconf in your project urls.py like this::

    `url(r'^auth/', include('maro_auth.urls', namespace='maro_auth')),`

4. Run `python manage.py migrate` to create the auth models.

5. Add the following settings to your `settings.py`:

    `INDEX_URL_NAME = 'index'` _name_ of your project's index url

    `PROFILE_URL_NAME = 'profile'` _name_ of your project's profile url

    `SITE_URL = 'http://localhost:8000'` your site's `url`, without the `/` at the end

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

