from django.core.checks import Error, Warning, register
from django.db.utils import ProgrammingError, OperationalError
from . import settings
from .models import Execution


@register()
def check_has_been_cleaned(app_configs, **kwargs):
    errors = []
    try:
        execution_count = Execution.objects.count()
    except (ProgrammingError, OperationalError):
        errors.append(
            Warning(
                "Birdbath is installed but migrations have not been ran.",
                hint="Run migrate to add birdbath tables.",
                id="birdbath.W001",
            )
        )
        return errors

    if settings.BIRDBATH_REQUIRED and not execution_count:
        errors.append(
            Error(
                "BIRDBATH_REQUIRED is set to True but `run_birdbath` has not been ran on this application",
                hint="If this is a production instance, set BIRDBATH_REQUIRED to False, otherwise, run the `run_birdbath` management command to clean data.",
                id="birdbath.E001",
            )
        )

    return errors
