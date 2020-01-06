from uuid import uuid4
from os.path import join

from django.db.models import (EmailField, CharField, BooleanField, Model,
                              ForeignKey, IntegerField, DecimalField, ImageField,
                              ManyToManyField, CASCADE)
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.conf import settings


def recipe_image_file_path(instance, filename):
    """Generate filepath for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid4}().{ext}'

    return join('uploads/recipe/', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = EmailField(max_length=255, unique=True)
    name = CharField(max_length=255)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(Model):
    """Tag to be used for a recipe"""

    name = CharField(max_length=255)
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def __str__(self):
        return self.name


class Ingredient(Model):
    """Ingredient to be used for a recipe"""

    name = CharField(max_length=255)
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def __str__(self):
        return self.name


class Recipe(Model):
    """Recipe object"""

    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    title = CharField(max_length=255)
    time_minutes = IntegerField()
    price = DecimalField(max_digits=5, decimal_places=2)
    link = CharField(max_length=255, blank=True)
    ingredients = ManyToManyField('Ingredient')
    tags = ManyToManyField('Tag')
    image = ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
