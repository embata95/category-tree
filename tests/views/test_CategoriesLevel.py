import tempfile
from django.urls import reverse
from eBag_task.categories.models import Category
from tests.core import CoreTest


class CategoriesLevelTestCase(CoreTest):
    def test_level_1(self):
        Category.objects.create(
            name="third object",
            description="Some description that doesn't matter",
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
        )
        returned_json = self.get_response_json(reverse("levels-list", kwargs={'level': 1}))
        category1 = {
            "id": 1,
            "name": "First object",
            "description": "Some description that doesn't matter",
            "image": returned_json[0]['image'],
            'similar_categories': ['Second object']
        }
        category3 = {
            "id": 3,
            "name": "third object",
            "description": "Some description that doesn't matter",
            "image": returned_json[1]['image'],
            'similar_categories': []
        }

        self.assertEqual(returned_json, [category1, category3])

        returned_json = self.get_response_json(reverse("levels-list", kwargs={'level': 2}))
        category2 = {
            "id": 2,
            "name": "Second object",
            "description": "Some other description that doesn't matter",
            "image": returned_json[0]['image'],
            'similar_categories': ['First object']
        }
        self.assertEqual(returned_json, [category2])
