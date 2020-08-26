from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    ROLES = [('admin', 'admin'), ('moderator', 'moderator'), ('user', 'user')]

    username = models.CharField(max_length=40, blank=True,
                                null=True, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLES,
                            default='user', verbose_name='Роль пользователя')
    bio = models.TextField(blank=True, verbose_name='Краткая биография')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username
