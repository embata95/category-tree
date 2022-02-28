from django.contrib import admin
from eBag_task.categories.models import Category


class RoleInline(admin.StackedInline):
    model = Category
    filter_horizontal = 'parent'


class RelationAdmin(admin.ModelAdmin):
    inlines = [RoleInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')


admin.site.register(Category, CategoryAdmin)
