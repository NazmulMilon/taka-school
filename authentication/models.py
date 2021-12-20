from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from authentication.managers import UserManager
from authentication.utils import random_hex_code


class User(AbstractBaseUser, PermissionsMixin):
    hashed_id = models.CharField(
        null=True,
        blank=True,
        max_length=16,
        unique=True
    )
    name = models.CharField(max_length=256)
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=25, unique=True)
    phone = models.CharField(max_length=12)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.pk:
            # Only set added_by during the first save.
            self.hashed_id = random_hex_code(length=16)
        super().save(*args, **kwargs)
