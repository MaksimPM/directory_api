from django.urls import path, include
from rest_framework.routers import DefaultRouter

from directory.apps import DirectoryConfig
from directory.views import MaterialViewSet, CategoryViewSet


app_name = DirectoryConfig.name

router = DefaultRouter()
router.register(r'materials', MaterialViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
