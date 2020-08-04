from birdbath.processors import BaseProcessor
from wagtail.contrib.forms.models import FormSubmission
from wagtail.search.models import Query


class SearchQueryCleaner(BaseProcessor):
    """ Removes all search queries """

    def run(self, **kwargs):
        Query.objects.all().delete()


class FormSubmissionCleaner(BaseProcessor):
    """ Removes all form submissions  """

    def run(self, **kwargs):
        FormSubmission.objects.all().delete()
