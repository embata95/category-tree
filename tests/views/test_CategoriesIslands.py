import tempfile

from django.urls import reverse

from eBag_task.categories.models import Category
from tests.core import CoreTest


class CategoriesIslandsTestCase(CoreTest):
    def test_get_islands(self):
        obj3 = Category.objects.create(
            name="Third object",
            description="Some description that doesn't matter",
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            parent=None
        )
        returned_json = self.get_response_json(reverse("islands-list"))
        self.assertEqual(returned_json, [{'members': ['First object', 'Second object']}])

        obj4 = Category.objects.create(
            name="Fourth object",
            description="Some description that doesn't matter",
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            parent=None
        )
        obj4.similar_to.add(obj3)

        returned_json = self.get_response_json(reverse("islands-list"))
        self.assertEqual(returned_json, [
            {'members': ['First object', 'Second object']},
            {'members': ['Third object', 'Fourth object']}
        ])
