from django.urls import path, include
from rest_framework import routers

from categories.views import CategoriesRoot, SimpleCategories, CategoriesLevel, CategoriesByParent, \
    CategoriesSimilarity, CategoriesIslands

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'roots', CategoriesRoot, basename='roots')
router.register(r'categories', SimpleCategories, basename='categories')
router.register(r'levels/(?P<level>\d+)', CategoriesLevel, basename='levels')
router.register(r'children/(?P<parent>\d+)', CategoriesByParent, basename='children')
router.register(r'similarity', CategoriesSimilarity, basename='similarity')
# router.register(r'rabbithole', LongestRabbitHole, basename='rabbithole')
router.register(r'islands', CategoriesIslands, basename='islands')

urlpatterns = [
    path('', include(router.urls)),
]
