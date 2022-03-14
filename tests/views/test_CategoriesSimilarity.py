import tempfile
from django.urls import reverse
from categories.models import Category
from tests.core import CoreTest


class CategoriesSimilarityTestCase(CoreTest):
    def test_get_categories(self):
        obj3 = Category.objects.create(
            name="Third object",
            description="Some description that doesn't matter",
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            parent=None
        )
        obj3.similar_to.add(self.first_obj, self.second_obj)

        returned_json = self.get_response_json(reverse("similarity-list"))
        category1 = {
            "id": 1,
            "name": "First object",
            "description": "Some description that doesn't matter",
            "image": returned_json[0]['image'],
            'similar_categories': [
                {
                    "id": 2,
                    "name": "Second object",
                    "description": "Some other description that doesn't matter"
                },
                {
                    "id": 3,
                    "name": "Third object",
                    "description": "Some description that doesn't matter"
                }
            ]
        }
        category2 = {
            "id": 2,
            "name": "Second object",
            "description": "Some other description that doesn't matter",
            "image": returned_json[1]['image'],
            'similar_categories': [
                {
                    "id": 1,
                    "name": "First object",
                    "description": "Some description that doesn't matter"
                },
                {
                    "id": 3,
                    "name": "Third object",
                    "description": "Some description that doesn't matter"
                }
            ]
        }
        category3 = {
            "id": 3,
            "name": "Third object",
            "description": "Some description that doesn't matter",
            "image": returned_json[2]['image'],
            'similar_categories': [
                {
                    "id": 1,
                    "name": "First object",
                    "description": "Some description that doesn't matter"
                },
                {
                    "id": 2,
                    "name": "Second object",
                    "description": "Some other description that doesn't matter"
                }
            ]
        }
        self.assertEqual(returned_json, [category1, category2, category3])

    def test_add_similar_categories(self):
        obj3 = Category.objects.create(
            name="Third object",
            description="Some description that doesn't matter",
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            parent=None
        )
        self.client.patch(reverse("similarity-detail", kwargs={'pk': 1}), data={
            "similar_to": [3],
        },  content_type='application/json')
        returned_json = self.get_response_json(reverse("similarity-detail", kwargs={'pk': 1}))
        category1 = {
            "id": 1,
            "name": "First object",
            "description": "Some description that doesn't matter",
            "image": returned_json['image'],
            'similar_categories': [
                {
                    "id": 3,
                    "name": "Third object",
                    "description": "Some description that doesn't matter"
                }
            ]
        }
        self.assertEqual(returned_json, category1)

    def test_delete_similar_categories(self):
        self.client.delete(reverse("similarity-detail", kwargs={'pk': 1}))
        returned_json = self.get_response_json(reverse("similarity-detail", kwargs={'pk': 1}))
        category1 = {
            "id": 1,
            "name": "First object",
            "description": "Some description that doesn't matter",
            "image": returned_json['image'],
            'similar_categories': []
        }
        self.assertEqual(returned_json, category1)

    def test_extra_kwargs_for_fields(self):
        obj3 = Category.objects.create(
            name="Third object",
            description="Some description that doesn't matter",
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            parent=None
        )
        self.client.patch(reverse("similarity-detail", kwargs={'pk': 1}), data={
            "id": "Shouldn't matter",
            "name": "Shouldn't matter",
            "description": "Shouldn't matter",
            "image": "Shouldn't matter",
            "similar_to": [3],
            "similar_categories": "Shouldn't matter"
        },  content_type='application/json')
        returned_json = self.get_response_json(reverse("similarity-detail", kwargs={'pk': 1}))
        category1 = {
            "id": 1,
            "name": "First object",
            "description": "Some description that doesn't matter",
            "image": returned_json['image'],
            'similar_categories': [
                {
                    "id": 3,
                    "name": "Third object",
                    "description": "Some description that doesn't matter"
                }
            ]
        }
        self.assertEqual(returned_json, category1)
