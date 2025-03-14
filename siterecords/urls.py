from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('records.urls')),
    path('users/', include('users.urls', namespace="users")),
    path("__debug__/", include("debug_toolbar.urls")),
]

handler404 = lambda request, exception: HttpResponseNotFound('<h1>Страница не найдена</h1>')

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Разделы для администрирования"
