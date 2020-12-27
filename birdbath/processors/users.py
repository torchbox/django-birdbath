from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from birdbath.settings import (
    BIRDBATH_USER_ANONYMISER_EXCLUDE_EMAIL_RE,
    BIRDBATH_USER_ANONYMISER_EXCLUDE_SUPERUSERS,
)

from .base import BaseModelAnonymiser


class BaseUserAnonymiser(BaseModelAnonymiser):
    model = get_user_model()

    def get_queryset(self):
        queryset = super().get_queryset()

        if BIRDBATH_USER_ANONYMISER_EXCLUDE_SUPERUSERS:
            queryset = queryset.exclude(is_superuser=True)

        if BIRDBATH_USER_ANONYMISER_EXCLUDE_EMAIL_RE:
            queryset = queryset.exclude(
                email__regex=BIRDBATH_USER_ANONYMISER_EXCLUDE_EMAIL_RE
            )

        return queryset


class UserEmailAnonymiser(BaseUserAnonymiser):
    anonymise_fields = ["email"]


class UserPasswordAnonymiser(BaseUserAnonymiser):
    anonymise_fields = ["password"]

    def generate_password(self, field, obj):
        return make_password(self.get_random_string())
