from django.http import HttpResponse
from rest_framework import viewsets
from eBag_task.categories.models import Category
from eBag_task.categories.serializers import CategoriesRootSerializer, SimpleCategoriesSerializer, \
    CategoriesSimilaritySerializer


class CategoriesRoot(viewsets.ModelViewSet):
    http_method_names = ["get"]

    def get_queryset(self):
        if 'pk' in self.kwargs and Category.objects.filter(pk=self.kwargs['pk']).exists():
            return Category.objects.filter(pk=self.kwargs['pk'])
        return Category.objects.filter(parent__isnull=True)
    serializer_class = CategoriesRootSerializer


class SimpleCategories(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = SimpleCategoriesSerializer


class CategoriesLevel(viewsets.ModelViewSet):
    http_method_names = ["get"]
    temp_queryset = Category.objects.filter(name__isnull=True)

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

    serializer_class = SimpleCategoriesSerializer


class CategoriesByParent(viewsets.ModelViewSet):
    http_method_names = ["get"]

    def get_queryset(self):
        pk = self.kwargs['parent']
        if pk.isnumeric() and Category.objects.filter(pk=pk).exists():
            return Category.objects.get(pk=pk).children.all()
    serializer_class = SimpleCategoriesSerializer


class CategoriesSimilarity(viewsets.ModelViewSet):

    def destroy(self, request, *args, **kwargs):
        if 'pk' in self.kwargs:
            category = Category.objects.get(pk=self.kwargs['pk'])
            category.similar_to.set([])
            category.save()
            return HttpResponse(content="Successfully deleted!")
        return HttpResponse(status=400, content="Bad request!")
    queryset = Category.objects.all()
    serializer_class = CategoriesSimilaritySerializer


class ShortestRabbitHole(viewsets.ModelViewSet):
    http_method_names = ["get"]
    paths = {}
    start = None
    end = None

    def get_queryset(self):
        if 'start' in self.request.query_params and 'end' in self.request.query_params:
            self.start = self.request.query_params['start']
            self.end = self.request.query_params['end']
            if self.start.isnumber() and self.end.isnumber():
                self.start = int(self.start)
                self.end = int(self.start)

    pass




