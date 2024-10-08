import pytest
from wagtail.contrib.forms.models import FormSubmission
from wagtail.contrib.search_promotions.models import Query

from birdbath.processors.contrib.wagtail import (
    FormSubmissionCleaner,
    SearchQueryCleaner,
)


@pytest.mark.django_db
def test_search_query_cleaner():
    Query.objects.create(query_string="test query")
    assert Query.objects.count() == 1
    cleaner = SearchQueryCleaner()
    cleaner.run()
    assert Query.objects.count() == 0


@pytest.mark.django_db
def test_form_submission_cleaner():
    FormSubmission.objects.create(
        form_data='{"name": "Test User", "email": "test@example.com"}',
        page_id=1,
    )
    assert FormSubmission.objects.count() == 1
    cleaner = FormSubmissionCleaner()
    cleaner.run()
    assert FormSubmission.objects.count() == 0
