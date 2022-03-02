from django.urls import reverse
from eBag_task.categories.models import Category
from tests.core import CoreTest


class SimpleCategoriesTestCase(CoreTest):
    def test_get_all_categories(self):
        returned_json = self.get_response_json(reverse("categories-list"))
        category1 = {
            "id": 1,
            "name": "First object",
            "description": "Some description that doesn't matter",
            "image": returned_json[0]['image'],
            'similar_categories': ['Second object']
        }
        category2 = {
            "id": 2,
            "name": "Second object",
            "description": "Some other description that doesn't matter",
            "image": returned_json[1]['image'],
            'similar_categories': ['First object']
        }
        self.assertEqual(returned_json, [category1, category2])

    def test_post_new_category(self):
        file = self.generate_photo_file()
        obj_data = {
            "name": "test_name",
            "description": "test_description",
            "image": file,
            "parent": 1,
            "similar_to": [1, 2],
        }
        self.client.post(reverse("categories-list"), data=obj_data, format="multipart/form-data")
        returned_json = self.get_response_json(reverse("categories-detail", kwargs={'pk': 3}))
        category3 = {
            "id": 3,
            "name": "test_name",
            "description": "test_description",
            "image": returned_json['image'],
            "similar_categories": ['First object', 'Second object'],
        }
        self.assertEqual(returned_json, category3)

    def test_delete_category(self):
        self.client.delete(reverse("categories-detail", kwargs={'pk': 1}))
        self.assertFalse(Category.objects.filter(pk=1).exists())
