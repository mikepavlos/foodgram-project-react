from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('recipes.urls')),
    path('api/', include('users.urls')),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
