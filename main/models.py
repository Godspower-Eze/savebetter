from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django_extensions.db.models import TimeStampedModel
from django.core.validators import RegexValidator

from .managers import UserManager

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'

ETH_ADDRESS_REGEX = '^0x[a-fA-F0-9]{40}$'


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    username = models.CharField(max_length=100, validators=[RegexValidator(regex=USERNAME_REGEX,
                                                                           message='Username must be alphanumeric or '
                                                                                   'contain numbers',
                                                                           code='Invalid username')], unique=True)
    first_name = models.CharField('first name', max_length=40, blank=True, null=True)
    last_name = models.CharField('last name', max_length=40, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """

        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='document/', default='default.png',
                                    help_text="Ensure your picture dimension is 300x300 in px ~Iykeln :)")

    address = models.CharField(max_length=42, validators=[RegexValidator(regex=ETH_ADDRESS_REGEX, 
                                                                             message="Enter a valid ethereum address", 
                                                                             code='Invalid address')], unique=True)

    def __str__(self):
        return f"{self.user.email}"