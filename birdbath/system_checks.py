import sys

from django.core.checks import Error, Warning, register
from django.db.utils import OperationalError, ProgrammingError

from . import settings
from .models import Execution


@register()
def check_has_been_cleaned(app_configs, **kwargs):
    # Skip check if it is running as part of a 'migrate' management command
    if sys.argv and len(sys.argv) > 1 and sys.argv[1] == "migrate":
        return []

    errors = []

    try:
        execution_count = Execution.objects.count()
    except (ProgrammingError, OperationalError):
        errors.append(
            Warning(
                "Birdbath is installed but migrations have not been run.",
                hint="Run migrate to add birdbath tables.",
                id="birdbath.W001",
            )
        )
        return errors

    if settings.BIRDBATH_REQUIRED and not execution_count:
        errors.append(
            Error(
                "BIRDBATH_REQUIRED is set to True but `run_birdbath` has not been run on this application",
                hint="If this is a production instance, set BIRDBATH_REQUIRED to False, otherwise, run the `run_birdbath` management command to clean data.",
                id="birdbath.E001",
            )
        )

    return errors
