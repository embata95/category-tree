import tempfile

from django.urls import reverse

from categories.models import Category
from categories.tests.core import CoreTest


class CategoriesByParentTestCase(CoreTest):
    def test_parent(self):
        returned_json = self.get_response_json(reverse("children-list", kwargs={'parent': 1}))
        category2 = {
            "id": 2,
            "name": "Second object",
            "description": "Some other description that doesn't matter",
            "image": returned_json[0]['image'],
            'similar_categories': [
                {'name': 'First object'}
            ]
        }
        self.assertEqual(returned_json, [category2])
        self.validate_get_only(reverse("children-list", kwargs={'parent': 1}))


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
            'similar_categories': [
                {'name': 'Second object'}
            ]
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
            'similar_categories': [
                {'name': 'First object'}
            ]
        }
        self.assertEqual(returned_json, [category2])


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
        Category.objects.create(
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
        Category.objects.create(
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


class SimpleCategoriesTestCase(CoreTest):
    def test_get_all_categories(self):
        returned_json = self.get_response_json(reverse("categories-list"))
        category1 = {
            "id": 1,
            "name": "First object",
            "description": "Some description that doesn't matter",
            "image": returned_json[0]['image'],
            'similar_categories': [
                {'name': 'Second object'}
            ]
        }
        category2 = {
            "id": 2,
            "name": "Second object",
            "description": "Some other description that doesn't matter",
            "image": returned_json[1]['image'],
            'similar_categories': [
                {'name': 'First object'}
            ]
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
            "similar_categories": [
                {'name': 'First object'},
                {'name': 'Second object'}
            ],
        }
        self.assertEqual(returned_json, category3)

    def test_delete_category(self):
        self.client.delete(reverse("categories-detail", kwargs={'pk': 1}))
        self.assertFalse(Category.objects.filter(pk=1).exists())
