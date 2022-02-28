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
        fields = ['id', 'name', 'description', 'image', 'subcategories']


class SimpleCategoriesSerializer(serializers.ModelSerializer):
    similar_categories = serializers.SerializerMethodField()

    def get_similar_categories(self, obj):
        return [curr_obj.name for curr_obj in obj.similar_to.all()]

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'parent', 'similar_to', 'similar_categories']
        extra_kwargs = {
            'parent': {'write_only': True},
            'similar_to': {'write_only': True, 'many': True},
            'similar_names': {'read_only': True}
        }


class CategoriesSimilaritySerializer(serializers.ModelSerializer):
    similar_categories = serializers.SerializerMethodField()

    def get_similar_categories(self, obj):
        return [{
            'id': curr_obj.id,
            'name': curr_obj.name,
            'description': curr_obj.description,
        } for curr_obj in obj.similar_to.all()]

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'similar_to', 'similar_categories']
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'read_only': True},
            'image': {'read_only': True},
            'description': {'read_only': True},
            'similar_categories': {'read_only': True},
            'similar_to': {'write_only': True}
        }
