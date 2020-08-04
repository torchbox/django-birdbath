import uuid
from typing import Pattern
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from birdbath.settings import (
    BIRDBATH_USER_ANONYMISER_EXCLUDE_EMAIL_RE,
    BIRDBATH_USER_ANONYMISER_EXCLUDE_SUPERUSERS,
)

from .base import BaseProcessor


class BaseUserAnonymiser(BaseProcessor):
    def get_queryset(self):
        users = get_user_model().objects.all()

        if BIRDBATH_USER_ANONYMISER_EXCLUDE_SUPERUSERS:
            users = users.exclude(is_superuser=True)

        if BIRDBATH_USER_ANONYMISER_EXCLUDE_EMAIL_RE:
            users = users.exclude(
                email__regex=BIRDBATH_USER_ANONYMISER_EXCLUDE_EMAIL_RE
            )

        return users


class UserEmailAnonymiser(BaseUserAnonymiser):
    def run(self):
        users = self.get_queryset()

        for user in users:
            user.email = f"{uuid.uuid4()}@example.com"

        get_user_model().objects.bulk_update(users, ["email"])


class UserPasswordAnonymiser(BaseUserAnonymiser):
    def run(self):
        users = self.get_queryset()

        for user in users:
            user.password = make_password(uuid.uuid4())

        get_user_model().objects.bulk_update(users, ["password"])
