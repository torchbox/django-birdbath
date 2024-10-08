import pytest
from django.core.management import call_command

from birdbath.models import Execution


@pytest.mark.django_db
def test_run_birdbath_command():
    assert Execution.objects.count() == 0
    call_command("run_birdbath")
    assert Execution.objects.count() == 1
