from rest_framework import serializers
from categories.models import Category


class CategoriesRootSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    def get_subcategories(self, obj):
        return CategoriesRootSerializer(obj.children.all(), many=True).data

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'subcategories']


class SimpleCategoriesSerializer(serializers.ModelSerializer):
    similar_categories = serializers.SerializerMethodField()

    def get_similar_categories(self, obj):
        return obj.similar_to.values('name')

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'parent', 'similar_to', 'similar_categories']
        extra_kwargs = {
            'parent': {'write_only': True},
            'similar_to': {'write_only': True, 'many': True},
            'similar_categories': {'read_only': True}
        }


class CategoriesSimilaritySerializer(serializers.ModelSerializer):
    similar_categories = serializers.SerializerMethodField()

    def get_similar_categories(self, obj):
        return obj.similar_to.values('id', 'name', 'description')

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
