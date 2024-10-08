import pytest

from birdbath.processors.users import UserEmailAnonymiser, UserPasswordAnonymiser


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="someone", email="someone@example.org", password="something"
    )


@pytest.mark.django_db
def test_user_email_anonymiser(user):
    original_email = user.email
    anonymiser = UserEmailAnonymiser()
    anonymiser.run()
    user.refresh_from_db()
    assert user.email != original_email
    assert "@" in user.email


@pytest.mark.django_db
def test_user_password_anonymiser(user, django_user_model):
    original_password_hash = user.password
    anonymiser = UserPasswordAnonymiser()
    anonymiser.run()
    user.refresh_from_db()
    assert user.password != original_password_hash
    assert not django_user_model.objects.get(username=user.username).check_password(
        "original_password"
    )
