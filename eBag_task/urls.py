from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from eBag_task import settings

urlpatterns = [
    path('admin', admin.site.urls),
    path('', include('eBag_task.categories.urls'), name='home_view')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
