import logging
import sys

from django.core.management.base import BaseCommand
from django.db import DatabaseError, transaction
from django.utils.module_loading import import_string

from birdbath.settings import BIRDBATH_CHECKS, BIRDBATH_PROCESSORS, BIRDBATH_SKIP_CHECKS
from birdbath.models import Execution

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run configured processors TSEST"
    requires_system_checks = []

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-checks", action="store_true", help="Skip running safety checks."
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            if not options.get("skip_checks"):
                for check_path in BIRDBATH_CHECKS:
                    check = import_string(check_path)()
                    if not check.check():
                        self.stderr.write(
                            f"Check {check_path} failed. Refusing to run processors."
                        )

                        return

            self.stdout.write("Beginning processing")

            errors = []

            for processor_path in BIRDBATH_PROCESSORS:
                self.stdout.write(f"Running processes: {processor_path}")
                processor = import_string(processor_path)()
                try:
                    processor.run()
                except Exception as e:
                    errors.append(e)

            if errors:
                raise Exception(errors)

            # Create a simple Execution object to track that this command has ran
            Execution.objects.create()

            self.stdout.write("Processing completed")

