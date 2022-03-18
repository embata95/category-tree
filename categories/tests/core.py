import io
import tempfile
from PIL import Image
from rest_framework.utils import json
from django.test import TestCase
from categories.models import Category


class CoreTest(TestCase):
    def setUp(self):
        self.first_obj = Category.objects.create(
            name="First object",
            description="Some description that doesn't matter",
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            parent=None
        )
        self.second_obj = Category.objects.create(
            name="Second object",
            description="Some other description that doesn't matter",
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            parent=self.first_obj
        )
        self.second_obj.similar_to.add(self.first_obj)

    def get_response_json(self, url):
        response = self.client.get(url, format='json')
        response.render()
        return json.loads(response.content)

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def validate_get_only(self, url):
        self.assertEqual(self.client.post(url).status_code, 405)
        self.assertEqual(self.client.delete(url).status_code, 405)
