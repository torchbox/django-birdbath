from django.core.checks import Error, register
from . import settings
from .models import Execution


@register()
def check_has_been_cleaned(app_configs, **kwargs):
    errors = []
    execution_count = Execution.objects.count()

    if settings.BIRDBATH_REQUIRED and not execution_count:
        errors.append(
            Error(
                "BIRDBATH_REQUIRED is set to True but `run_birdbath` has not been ran on this application",
                hint="If this is a production instance, set BIRDBATH_REQUIRED to False, otherwise, run the `run_birdbath` management command to clean data.",
                id="birdbath.E001",
            )
        )

    return errors
