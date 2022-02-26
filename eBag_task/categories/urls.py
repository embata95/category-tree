from django.urls import path, include
from rest_framework import routers

from eBag_task.categories.views import CategoriesRoot, SimpleCategories, CategoriesLevel, CategoriesByParent, \
    ShortestRabbitHole, CategoriesSimilarity

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'roots', CategoriesRoot, basename='roots')
router.register(r'categories', SimpleCategories, basename='categories')
router.register(r'levels/(?P<level>\d+)', CategoriesLevel, basename='levels')
router.register(r'children/(?P<parent>\d+)', CategoriesByParent, basename='children')
router.register(r'similarity', CategoriesSimilarity, basename='similarity')
router.register(r'rabbithole', ShortestRabbitHole, basename='rabbithole')

urlpatterns = [
    path('', include(router.urls)),
]
