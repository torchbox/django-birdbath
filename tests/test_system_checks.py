import pytest
from django.core.checks import Error
from django.core.management import call_command

from birdbath.system_checks import check_has_been_cleaned


@pytest.mark.django_db
def test_check_has_been_cleaned():
    # Test when Birdbath hasn't been run
    errors = check_has_been_cleaned(None)
    assert len(errors) == 1
    assert isinstance(errors[0], Error)
    assert errors[0].id == "birdbath.E001"

    # Run Birdbath
    call_command("run_birdbath")

    # Test after Birdbath has been run
    errors = check_has_been_cleaned(None)
    assert len(errors) == 0
