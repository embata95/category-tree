from django.urls import reverse

from tests.core import CoreTest


class CategoriesByParentTestCase(CoreTest):
    def test_parent(self):
        returned_json = self.get_response_json(reverse("children-list", kwargs={'parent': 1}))
        category2 = {
            "id": 2,
            "name": "Second object",
            "description": "Some other description that doesn't matter",
            "image": returned_json[0]['image'],
            'similar_categories': ['First object']
        }
        self.assertEqual(returned_json, [category2])
        self.validate_get_only(reverse("children-list", kwargs={'parent': 1}))
