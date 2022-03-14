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
        self.all_visited_keys = []

    def get_island_ids(self, obj, visited_combinations=[]):
        for curr_node in obj.similar_to.all():
            ids = [obj.id, curr_node.id]
            key = f"{min(ids)}_{max(ids)}"
            if key not in self.all_visited_keys:
                visited_combinations.append(key)
                self.all_visited_keys.append(key)
                self.get_island_ids(curr_node, visited_combinations)
        ids = (set([int(num) for combination in visited_combinations for num in combination.split('_')]))
        return None or ids

    def list(self, request, *args, **kwargs):
        result = []
        for curr_obj in Category.objects.all():
            curr_island = self.get_island_ids(curr_obj, [])
            if curr_island:
                result.append([Category.objects.filter(id__in=curr_island)])
        islands = [island for island in result]
        return Response([{"members": [obj.name for obj in island[0]]} for island in islands])


class LongestRabbitHole(viewsets.ModelViewSet):
    # Again use memoisation to make O(N) complexity
    # open rabbit holes and closed (circular)
    # Open holes -> start and end only with one similar
    # Iterate over all connections and aggregate the straight parts where possible and create a conjunction table
    # Record all visited nodes and check if any are not visited (should be single nodes not part of rabbit hole or circles)
    # Again, if no movement available, return -> this will open the closed holes
    pass
