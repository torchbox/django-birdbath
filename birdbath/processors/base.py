import string

from django.db import models
from django.utils.crypto import get_random_string
from django.utils.functional import cached_property

from faker import Faker

LOWERCASE_STRING = "".join(string.ascii_lowercase)
UPPERCASE_STRING = "".join(string.ascii_uppercase)
NUMBER_FIELD_TYPES = (models.IntegerField, models.FloatField, models.DecimalField)
FIRST_NAME_FIELDS = ("first_name", "forename", "given_name", "middle_name")
LAST_NAME_FIELDS = ("last_name", "surname", "family_name")

RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class BaseProcessor:
    def run(self):
        raise NotImplementedError


class BaseModelProcessor(BaseProcessor):
    model = None

    def get_queryset(self):
        return self.model.objects.all()


class BaseModelDeleter(BaseModelProcessor):
    bulk_delete = True

    def run(self, **kwargs):
        queryset = self.get_queryset()
        if self.bulk_delete:
            return queryset.delete()
        for obj in queryset:
            obj.delete()


class BaseModelAnonymiser(BaseModelProcessor):
    """
    A processor that can be subclassed to annonymise or clear field values for
    a specific model.

    Update ``clear_fields`` with names of fields you would like to 'clear' the
    value for. If the field uses ``null=True`` in its definition, values will
    be set to ``None``. Otherwise, the processor will attempt to set the field
    to a falsey value.

    Update ``anonymise_fields`` with names of fields you would like to generate
    random replacement values for. Valid replacement values will be
    automatically generated for any field with ``choices`` set, or an instance
    of one of the following field types:

    * ``django.db.models.field.EmailField``
    * ``django.db.models.field.DateField``
    * ``django.db.models.field.DateTimeField``
    * ``django.db.models.field.CharField``
    * ``django.db.models.field.TextField``
    * ``django.db.models.field.IntegerField``
    * ``django.db.models.field.FloatField``
    * ``django.db.models.field.DecimalField``

    If you have fields with custom validation requirements, or would simply
    like to generate more realistic replacement values, you can add 'generate'
    methods to your subclass to achieve this. ``BaseModelAnonymiser`` will
    automatically look for a method matching the format
    "generate_{field_name}". For example, the following processor will set
    fixed values for 'account_number' and 'sort_code' fields, and use the
    processor's `faker` instance to generate a new value for 'account_holder':

    .. code-block:: python

        from birdbath.processors.base import BaseModelAnonymiser

        class DirectDebitDeclarationAnonymiser(BaseModelAnonymiser):

            model = DirectDebitDeclaration
            anonymise_fields = ["account_holder", "account_number", "sort_code"]

            def generate_account_holder(self, field, obj):
                # Return a value to replace 'account_holder' field values
                # `field` is the field instance from the model
                # `obj` is the model instance being updated
                return self.faker.name()

            def generate_account_number(self, field, obj):
                # Return a value to replace 'account_number' field values
                # `field` is the field instance from the model
                # `obj` is the model instance being updated
                return '55779911'

            def generate_sort_code(self, field, obj):
                # Return a value to replace 'sort_code' field values
                # `field` is the field instance from the model
                # `obj` is the model instance being updated
                return '200000'
    """

    clear_fields = []
    anonymise_fields = []
    bulk_update = True

    @cached_property
    def faker(self):
        f = Faker()
        Faker.seed(0)
        return f

    @cached_property
    def update_fields(self):
        fields = set(self.anonymise_fields)
        fields.update(self.clear_fields)
        return fields

    def get_random_integer(self, min_value=0, max_value=9999):
        return self.faker.pyint(min_value, max_value)

    def get_random_string(
        self,
        min_length=1,
        max_length=50,
        length=None,
        allowed_chars=RANDOM_STRING_CHARS,
    ):
        length = length or self.faker.pyint(min_length, max_length)
        return get_random_string(length, allowed_chars=allowed_chars)

    def get_random_lowercase_string(self, min_length=1, max_length=50, length=None):
        return self.get_random_string(min_length, max_length, length, LOWERCASE_STRING)

    def get_random_uppercase_string(self, min_length=1, max_length=50, length=None):
        return self.get_random_string(min_length, max_length, length, UPPERCASE_STRING)

    def get_random_email(self, max_length=200, domain="example.com"):
        name = self.get_random_lowercase_string(3, max_length - (len(domain) + 1))
        return f"{name}@{domain}"

    def generate_field_value(self, field, field_name, obj):
        if field.choices is not None:
            random_index = self.faker.pyint(0, len(field.choices)) - 1
            return field.choices[random_index][0]
        if isinstance(field, models.EmailField):
            return self.get_random_email(field.max_length)
        if isinstance(field, models.DateField):
            return self.faker.past_date()
        if isinstance(field, NUMBER_FIELD_TYPES):
            return self.get_random_integer(field.min_value, field.max_value)
        if field_name in FIRST_NAME_FIELDS:
            return self.faker.first_name()
        if field_name in LAST_NAME_FIELDS:
            return self.faker.last_name()
        return self.get_random_string(max_length=getattr(field, "max_length", 50))

    def get_anonymised_field_value(self, field, field_name, obj):
        generate_method = getattr(self, f"generate_{field_name}", None)
        if generate_method is not None:
            return generate_method(field, obj)
        return self.generate_field_value(field, field_name, obj)

    def get_cleared_field_value(self, field, field_name, obj):
        if field.null:
            return None
        if isinstance(field, NUMBER_FIELD_TYPES):
            return 0
        return ""

    def run(self, **kwargs):
        queryset = self.get_queryset()
        for obj in queryset:
            self.process_object(obj)
        self.save_changes(queryset)

    def process_object(self, obj):
        for field_name in self.anonymise_fields:
            f = self.model._meta.get_field(field_name)
            value = self.get_anonymised_field_value(f, field_name, obj)
            setattr(obj, field_name, value)

        for field_name in self.clear_fields:
            f = self.model._meta.get_field(field_name)
            value = self.get_cleared_field_value(f, field_name, obj)
            setattr(obj, field_name, value)

    def save_changes(self, object_list):
        if self.bulk_update:
            return self.model.objects.bulk_update(object_list, self.update_fields)
        for obj in object_list:
            obj.save(update_fields=self.update_fields)
