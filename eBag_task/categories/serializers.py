from rest_framework import serializers
from eBag_task.categories.models import Category


class CategoriesRootSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    def get_subcategories(self, obj):
        if obj.children.all() is not None:
            return [CategoriesRootSerializer(instance=curr_child).data for curr_child in obj.children.all()]
        else:
            return None

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'subcategories']


class SimpleCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'parent', 'similar_to']
        extra_kwargs = {
            'parent': {'write_only': True},
            'similar_to': {'write_only': True, 'many': True}
        }


class CategoriesSimilaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'similar_to']
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'read_only': True},
            'image': {'read_only': True}
        }
