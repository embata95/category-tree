from categories.tests.common_test_set_up import CoreTest
from categories.models import Category


class CategoryTestCase(CoreTest):
    def test_parent_is_set_correctly(self):
        self.assertEqual(self.second_obj.parent, self.first_obj)

    def test_similar_to_is_set_correctly_and_simetric(self):
        self.assertTrue(self.first_obj in self.second_obj.similar_to.all())
        self.assertTrue(self.second_obj in self.first_obj.similar_to.all())

        self.second_obj.similar_to.remove(self.first_obj)

        self.assertFalse(self.first_obj in self.second_obj.similar_to.all())
        self.assertFalse(self.second_obj in self.first_obj.similar_to.all())

    def test_self_parent_error(self):
        temp_obj = self.second_obj
        temp_obj.parent = self.second_obj
        self.assertRaises(ValueError, temp_obj.save)

    def test_self_similar_error(self):
        temp_obj = self.second_obj
        self.assertRaises(ValueError, temp_obj.similar_to.add, self.second_obj)

    def test_on_delete_cascade(self):
        self.first_obj.delete()
        self.assertFalse(Category.objects.exists())
