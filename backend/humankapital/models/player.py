from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy
from .manager import EmailUserManager
from rest_framework import serializers


class Player(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    objects = EmailUserManager()

    is_staff = models.BooleanField(
        ugettext_lazy('staff status'),
        default=False,
        help_text=ugettext_lazy('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        ugettext_lazy('active'),
        default=True,
        help_text=ugettext_lazy(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'

    balance = models.IntegerField(default=0)
    karma = models.FloatField(default=1)


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("balance","karma")

