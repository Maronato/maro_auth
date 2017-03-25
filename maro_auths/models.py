from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from .email_helpers import welcome_email, send_change_email


class EmailManager(models.Model):
    """Email Manager
    Handles the email verification process
    Also handles the email sending process
    """

    # user obj associated with this manager
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    # other, unverified(or outdated) email
    other_email = models.EmailField(blank=True, null=True)
    # is the user active? i.e. has he/she already verified their current email?
    active = models.BooleanField(default=False)
    # the user's key
    key = models.CharField(max_length=40, unique=True)

    # Returns the User's current active(?) email
    @property
    def active_email(self):
        return self.user.email

    # True if the current active_email is the right one. False if there is an active verification process
    @property
    def is_active(self):
        return self.active

    def generate_key():
        """Generate Key
        Uses Django's built-in methods to generate a random key that is unique
        """
        # generate random key
        key = get_random_string()

        # if it's already taken, generate another
        if EmailManager.objects.filter(key=key).exists():
            return EmailManager.generate_key()

        # return it
        return key

    def create(user):
        """Create (or Update) Email
        Check if the user has an emailmanager
        if does not, create one and return it.
        if does, return it.
        """
        # if the user does not have an email manager yet, create it
        if not EmailManager.objects.filter(user=user).exists():

            # create a new email manager obj
            new = EmailManager(
                key=EmailManager.generate_key(),
                user=user
            )
            new.save()

            # Send confirmation email
            welcome_email(new)

        return user.emailmanager

    def confirm(key):
        """Confirms an email using key
        Confirms the email, changing the active email or activating it
        only does so if the future active email is not being used by nobody else
        """
        manager = EmailManager.find_key(key)
        if not manager:
            # If key is wrong, return False
            return False

        if manager.is_active:
            # Do not reactivate users
            return False

        if manager.other_email:
            # If other_email
            if EmailManager.email_used(manager.other_email):
                # Other_email already being used by someone
                return False
            # Other email is not being used by anybody else, make it the active one

            # if username == email, set it as new email
            if manager.user.email == manager.user.username:
                manager.user.username = manager.other_email
            manager.user.email = manager.other_email
            manager.user.is_active = True
            manager.user.save()
        else:
            manager.user.is_active = True
            manager.user.save()

        # Activate email
        manager.active = True
        manager.save()

        # Returns the activated User's obj
        return manager.user

    def change_email(self, email):
        """Change Email
        Allows users to change their email, gerating a key
        """
        self.active = False
        self.other_email = email
        self.key = EmailManager.generate_key()
        self.save()

        send_change_email(self, email)
        return self.key

    def email_used(email):
        # True if user exists and is active (email taken and being used)
        user = User.objects.filter(email=email)
        return True if user.exists() and user.is_active else False

    def find_key(key):
        # Returns an Email_Manager obj if a key exists, False otherwise
        return EmailManager.objects.get(key=key) if EmailManager.objects.filter(key=key).exists() else False

    def __str__(self):
        return "Manager de " + self.user.email
