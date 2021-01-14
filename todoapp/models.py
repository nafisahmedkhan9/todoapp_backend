from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.conf import settings
import jwt


TASK_COMPLETION_STATUS = (
    ("Pending", "Pending"),
    ("Progress", "Progress"),
    ("Completed", "Completed"),
)

# this can be changed to 1,2,3 if words are ambiguous in this context
PRIORITIES = (
    ('Normal', "Normal"),
    ('Important', "Important"),
    ('Urgent', "Urgent")
)


class UserManager(BaseUserManager):

    def create_user(self, email, password):
        # create and return user with email, username and password
        if email is None:
            raise TypeError('User must have an email')
        if password is None:
            raise TypeError('User must have a password')

        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        # create and return user with superuser (admin) permission
        if password is None:
            raise TypeError('Superuser must have a password')
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        if password is not None:
            user.set_password(password)
        user.save()

        return user

    def create_user_without_password(self, email):
        user = self.model(email=email)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(db_index=True, unique=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'email'
    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return str(self.email)

    def to_dict(self):
        return {
            'email': self.email,
            'name': self.name,
            'id': self.pk,
        }

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')


class Bucket(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __str__(self):
        return str(self.name)


class CustomManager(models.Manager):
    def get_user_filtered(self, user):
        if user.is_superuser:
            return self.all()
        else:
            return self.filter(user=user)


class Task(models.Model):
    user = models.ForeignKey(
        'User', null=True, related_name='user_tasks', on_delete=models.CASCADE)
    bucket = models.ForeignKey(
        "Bucket", null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITIES)
    status = models.CharField(max_length=20, choices=TASK_COMPLETION_STATUS)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomManager()

    def __unicode__(self):
        return self.description

    def __str__(self):
        return str(self.description)
