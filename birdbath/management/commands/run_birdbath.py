import logging

from birdbath.settings import BIRDBATH_CHECKS, BIRDBATH_PROCESSORS, BIRDBATH_SKIP_CHECKS
from django.core.management.base import BaseCommand
from django.db import DatabaseError, transaction
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run configured processors"

    def handle(self, *args, **options):
        with transaction.atomic():
            if not BIRDBATH_SKIP_CHECKS:
                for check_path in BIRDBATH_CHECKS:
                    check = import_string(check_path)()
                    if not check.check():
                        logger.error(
                            f"Check {check_path} failed. Refusing to run processors."
                        )
                        return

            logger.info("Beginning processing")

            for processor_path in BIRDBATH_PROCESSORS:
                logger.info(f"Running processes: {processor_path}")
                processor = import_string(processor_path)()
                processor.run()
