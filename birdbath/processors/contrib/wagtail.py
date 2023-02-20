from wagtail.contrib.forms.models import FormSubmission
from wagtail.search.models import Query

from birdbath.processors import BaseModelDeleter


class SearchQueryCleaner(BaseModelDeleter):
    """Removes all search queries"""

    model = Query


class FormSubmissionCleaner(BaseModelDeleter):
    """Removes all form submissions"""

    model = FormSubmission
