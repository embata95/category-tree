from rest_framework import viewsets
from rest_framework.response import Response
from categories.models import Category
from categories.serializers import CategoriesRootSerializer, SimpleCategoriesSerializer, \
    CategoriesSimilaritySerializer


class CategoriesRoot(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = CategoriesRootSerializer

    def get_queryset(self):
        if 'pk' in self.kwargs and Category.objects.filter(pk=self.kwargs['pk']).exists():
            return Category.objects.filter(pk=self.kwargs['pk'])
        return Category.objects.filter(parent__isnull=True)


class SimpleCategories(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = SimpleCategoriesSerializer


class CategoriesLevel(viewsets.ModelViewSet):
    http_method_names = ["get"]
    temp_queryset = Category.objects.filter(name__isnull=True)
    serializer_class = SimpleCategoriesSerializer

    def find_level(self, queryset, level):
        if not queryset:
            return
        if level == 1:
            self.temp_queryset = self.temp_queryset.union(queryset)
            return
        for curr_child in queryset:
            self.find_level(
                queryset=curr_child.children.all(),
                level=level - 1
            )

    def get_queryset(self):
        level = 1
        if 'level' in self.kwargs and self.kwargs['level'].isnumeric():
            level = max(int(self.kwargs['level']), level)
        self.find_level(queryset=Category.objects.filter(parent__isnull=True), level=level)
        return self.temp_queryset


class CategoriesByParent(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = SimpleCategoriesSerializer

    def get_queryset(self):
        pk = self.kwargs['parent']
        if pk.isnumeric() and Category.objects.filter(pk=pk).exists():
            return Category.objects.get(pk=pk).children.all()


class CategoriesSimilarity(viewsets.ModelViewSet):
    http_method_names = ["get", "put", "patch", "delete"]
    queryset = Category.objects.all()
    serializer_class = CategoriesSimilaritySerializer

    def destroy(self, request, *args, **kwargs):
        if 'pk' in self.kwargs:
            category = Category.objects.get(pk=self.kwargs['pk'])
            category.similar_to.set([])
            category.save()
            return Response({"message": "Successfully cleared!"})
        return Response({"message": "Bad request!"})


class CategoriesIslands(viewsets.ReadOnlyModelViewSet):
    http_method_names = ["get"]
    queryset = Category.objects.none()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.visited_combinations = set()

    def get_island_ids(self, obj, curr_island=None):
        if not curr_island:
            curr_island = set()
        for curr_node in set(obj.similar_to.all()) - curr_island - self.visited_combinations:
            curr_island.add(obj)
            curr_island.add(curr_node)
            self.visited_combinations.add(obj)
            self.visited_combinations.add(curr_node)
            self.get_island_ids(curr_node, curr_island)
        return curr_island

    def list(self, request, *args, **kwargs):
        result = []
        for curr_obj in Category.objects.all():
            island = self.get_island_ids(curr_obj)
            if island:
                result.append(island)
        return Response([{'members': [obj.name for obj in temp_island]} for temp_island in result])
