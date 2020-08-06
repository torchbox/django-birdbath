from django.conf import settings

BIRDBATH_REQUIRED = getattr(settings, "BIRDBATH_REQUIRED", True,)

BIRDBATH_CHECKS = getattr(settings, "BIRDBATH_CHECKS", [],)
BIRDBATH_PROCESSORS = getattr(
    settings,
    "BIRDBATH_PROCESSORS",
    [
        "birdbath.processors.users.UserEmailAnonymiser",
        "birdbath.processors.users.UserPasswordAnonymiser",
    ],
)
BIRDBATH_SKIP_CHECKS = getattr(settings, "BIRDBATH_SKIP_CHECKS", False)

BIRDBATH_USER_ANONYMISER_EXCLUDE_EMAIL_RE = getattr(
    settings, "BIRDBATH_USER_ANONYMISER_EXCLUDE_EMAIL_RE", r"example\.com$"
)

BIRDBATH_USER_ANONYMISER_EXCLUDE_SUPERUSERS = getattr(
    settings, "BIRDBATH_USER_ANONYMISER_EXCLUDE_SUPERUSERS", True
)

