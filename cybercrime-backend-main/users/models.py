import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomizedUserManager(UserManager):
    def create_user(self, username, totp_secret, recovery_phrase, is_active=True, is_staff=False, password=None):
        """
        Creates and returns a new user with the given username and TOTP secret.
        """
        user = self.model(
            username=username,
            totp_secret=totp_secret,
            recovery_phrase_hash=make_password(recovery_phrase),
            is_active=is_active,
            is_staff=is_staff,
        )
        
        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()
            
        user.full_clean()
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    totp_secret = models.CharField(_('TOTP secret'), max_length=32, unique=True, blank=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    recovery_phrase_hash = models.CharField(max_length=256, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomizedUserManager()
    
    class Meta:
        db_table = 'users'
        managed = True  
    
    def __str__(self):
        return f"User(username={self.username})"