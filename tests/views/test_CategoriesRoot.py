import tempfile
from django.urls import reverse
from categories.models import Category
from tests.core import CoreTest


class CategoryRootTestCase(CoreTest):
    def test_all_roots(self):
        returned_json = self.get_response_json(reverse("roots-list"))
        root1 = {
            "id": 1,
            "name": "First object",
            "description": "Some description that doesn't matter",
            "image": returned_json[0]['image'],
            "subcategories": [
                {
                    "id": 2,
                    "name": "Second object",
                    "description": "Some other description that doesn't matter",
                    "image": returned_json[0]['subcategories'][0]['image'],
                    "subcategories": []
                }
            ]
        }
        expected_json = root1
        self.assertEqual(returned_json, [expected_json])

        Category.objects.create(
            name="Third object",
            description="Third description",
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )
        returned_json = self.get_response_json(reverse("roots-list"))
        root3 = {
            "id": 3,
            "name": "Third object",
            "description": "Third description",
            "image": returned_json[1]['image'],
            "subcategories": []
        }
        expected_json = [root1, root3]
        self.assertEqual(returned_json, expected_json)

        returned_json = self.get_response_json(reverse("roots-detail", kwargs={'pk': 1}))
        self.assertEqual(returned_json, root1)

        returned_json = self.get_response_json(reverse("roots-detail", kwargs={'pk': 3}))
        self.assertEqual(returned_json, root3)

        self.validate_get_only(reverse("roots-list"))
        self.validate_get_only(reverse("roots-detail", kwargs={'pk': 1}))
