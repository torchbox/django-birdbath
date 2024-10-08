DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "wagtail.contrib.forms",
    "wagtail.contrib.search_promotions",
    "wagtail.search",
    "wagtail.users",
    "wagtail",
    "birdbath",
]

SECRET_KEY = "not-so-secret-for-tests"

STATIC_URL = "/static/"
