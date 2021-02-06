from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
                                       BaseUserManager, \
                                       PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **other_fields):
        """Creates and saves a new user."""
        if not email:
            raise ValueError('Email must not be an empty field.')
        user = self.model(email=self.normalize_email(email), **other_fields)
        if not password:
            password = self.make_random_password()
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
