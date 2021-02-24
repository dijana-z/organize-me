from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
                                       BaseUserManager, \
                                       PermissionsMixin


class Household(models.Model):

    name = models.CharField(max_length=255, unique=True)
    grocery_list = models.ManyToManyField('Grocery', related_name='grocery')
    shopping_list = models.ManyToManyField('Grocery', related_name='shopping')


class UserManager(BaseUserManager):
    """Custom User Manager with helper functions."""
    def create_user(self, email, password=None, household='', **other_fields):
        """Creates and saves a new user."""
        if not email:
            raise ValueError('Email must not be an empty field.')
        user = self.model(email=self.normalize_email(email), **other_fields)
        if not password:
            password = self.make_random_password()
        user.set_password(password)
        if household:
            hh = Household.objects.get_or_create(name=household)[0]
            user.household = hh
            hh.save(using=self._db)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, household=''):
        """Creates and saves a new superuser."""
        user = self.create_user(email, password, household)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username."""

    # Add user model fields
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    household = models.ForeignKey(to=Household, on_delete=models.CASCADE,
                                  null=True)

    # Create user manager object
    objects = UserManager()

    # Replace login username field with email
    USERNAME_FIELD = 'email'


class Grocery(models.Model):
    """Custom grocery item."""
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    household = models.ForeignKey(to=Household,
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}: {self.quantity}'
