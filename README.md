# Django Birdbath

A simple tool for giving Django database data a good wash. Anonymise user data, delete stuff you don't need in your development environment, or whatever it is you need to do.

## Usage

1. Add `birdbath` to your `INSTALLED_APPS`
2. Set `BIRDBATH_CHECKS` and `BIRDBATH_PROCESSORS` as appropriate in your settings file (see Configuration below).
3. Run `./manage.py run_birdbath` to trigger processors.

Important! The default processors are destructive and will anonymise User emails and passwords. Do not run in production!

By default, Birdbath enables a [Django system check](https://docs.djangoproject.com/en/3.0/topics/checks/) which will trigger an error if a Birdbath cleanup has not been triggered on the current environment.

This is intended to give developers a hint that they need to anonymise/cleanup their data before running commands such as `runserver`.

The suggested approach is to set `BIRDBATH_REQUIRED` to `False` in production environments using an environment variable.

Checks can be skipped using the `--skip-checks` flag on `run_birdbath`.

## Configuration

### Common Settings

- `BIRDBATH_REQUIRED` (default: `True`) - if True, a Django system check will throw an error if anonymisation has not been executed. Set to `False` in your production environments.
- `BIRDBATH_CHECKS` - a list of paths to 'Check' classes to be executed before processors. If any of these returns False, the processors will refuse to run.
- `BIRDBATH_PROCESSORS` - a list of paths to 'Processor' classes to be executed to clean data.

### Processor Specific Settings

- `BIRDBATH_USER_ANONYMISER_EXCLUDE_EMAIL_RE` (default: `example\.com$`) - A regex pattern which will be used to exclude users that match a certain email address when anonymising.
- `BIRDBATH_USER_ANONYMISER_EXCLUDE_SUPERUSERS` (default: `True`) - If True, users with `is_superuser` set to True will be excluded from anonymisation.

## Implementing your Own

Your site will probably have some of your own check/processor needs.

### Checks

Custom checks can be implemented by subclassing `birdbath.checks.BaseCheck` and implementing the `check` method:

```
from birdbath.checks import BaseCheck


class IsDirtyCheck(BaseCheck):
    def check(self):
        return os.environ.get("IS_DIRTY")
```

The `check` method should either return `True` if the checks should continue, or `False` to stop checking and prevent processors from running.

### Processors

Custom processors can be implemented by subclassing `birdbath.processors.BaseProcessor` and implementing the `run` method:

```
from birdbath.processors import BaseProcessor


class DeleteAllMyUsersProcessor(BaseProcessor):
    def run(self):
        User.objects.all().delete()
```

There are also more specialised base classes in `birdbath.processors` that can help you write cleaner custom processors. For example, the above example could be written using the `BaseModelDeleter` class instead:

```
from birdbath.processors import BaseModelDeleter


class DeleteAllMyUsersProcessor(BaseModelDeleter):
    model = User
```

If you only need to delete a subset of users, you can override the `get_queryset()` method, like so:

```
from birdbath.processors import BaseModelDeleter


class DeleteNonStaffUsersProcessor(BaseModelDeleter):
    model = User

    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False)
```

If you're looking to 'anonymise' rather than delete objects, you will likely find the `BaseModelAnonymiser` class useful. You just need to indicate the fields that should be 'anonymised' or 'cleared', and the class will do the rest. For example:


```
from birdbath.processors import BaseModelAnonymiser


class UserAnonymiser(BaseModelAnonymiser):
    model = User

    # generate random replacement values for these fields
    anoymise_fields = ["first_name", "last_name", "email", "password"]


class CustomerProfileAnonymiser(BaseModelAnonymiser):
    model = CustomerProfile

    # generate random replacement values for these fields
    anoymise_fields = ["date_of_birth"]

    # set these fields to ``None`` (if supported), or a blank string
    clear_fields = ["email_consent", "sms_consent", "phone_consent", "organisation"]
```

The class will generate:
- Valid but non-existent email addresses for fields using `django.db.models.EmailField`.
- Random choice selections for any field with `choices` defined at the field level.
- Historic dates for fields using `django.db.models.DateField` or `django.db.models.DateTimeField`.
- Random numbers for fields using `django.db.models.IntegerField` (or one of it's subclasses), `django.db.models.FloatField` or `django.db.models.DecimalField`.
- Real-looking first names for fields with one of the following names: `"first_name"`, `"forename"`, `"given_name"`, `"middle_name"`.
- Real-looking last names for fields with one of the following names:
`"last_name"`, `"surname"`, `"family_name"`.
- Random strings for any other fields using `django.db.models.CharField`, `django.db.models.TextField` or a subclass of those.

 If you have fields with custom validation requirements, or would simply like to generate more realistic replacement values, you can add 'generate' methods to your subclass to achieve this. `BaseModelAnonymiser` will automatically look for method matching the format `"generate_{field_name}"` when anoymising field values. For example, the following processor will generate random values for "account_holder" and "account_number" fields:

```
from birdbath.processors import BaseModelAnonymiser


class DirectDebitDeclarationAnonymiser(BaseModelAnonymiser):

    model = DirectDebitDeclaration
    anonymise_fields = ["account_holder", "account_number"]

    def generate_account_holder(self, field, obj):
        # Return a value to replace 'account_holder' field values
        # `field` is the field instance from the model
        # `obj` is the model instance being updated
        return self.faker.name()

    def generate_account_number(self, field, obj):
        # Return a value to replace 'account_number' field values
        # `field` is the field instance from the model
        # `obj` is the model instance being updated
        return self.faker.iban()
```


## Check/Processor Reference

### Checks

- `checks.contrib.heroku.HerokuNotProductionCheck` - fails if the `HEROKU_APP_NAME` environment variable is not set, or if it set and includes the word `production`.
- `checks.contrib.heroku.HerokuAnonymisationAllowedCheck` - fails if the `ALLOWS_ANONYMISATION` environment variable does not match the name of the application.

### Processors

- `processors.users.UserEmailAnonymiser` - replaces user email addresses with randomised addresses
- `processors.users.UserPasswordAnonymiser` - replaces user passwords with random UUIDs
- `processors.contrib.wagtail.SearchQueryCleaner` - removes the full search query history
- `processors.contrib.wagtail.FormSubmissionCleaner` - removes all form submissions
